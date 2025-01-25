import asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine
import json
import datetime

from config import cfg
from db import dbe
import models as m


class ImportData:
    def __init__(self, dbe: AsyncEngine):
        self.dbe = dbe

    async def run(self):
        async with self.dbe.begin() as dbc:
            query = (
                sa.select(
                    m.debt.c.id,
                    m.debt.c.name,
                    m.debt.c.date,
                    m.debt.c.amount,
                    m.debt.c.period,
                    m.debt.c.rate,
                    m.user.c.email.label("author_email"),
                    m.user.c.name.label("author_name"),
                )
                .select_from(m.debt)
                .order_by(m.debt.c.date)
            )
            query = query.where(m.user.c.email == m.debt.c.author_email)
            res = await dbc.execute(query)
            debts = res.fetchall()
            for d in debts:
                try:
                    with open(f"data/payments-{d.id}.json", mode="r") as f:
                        await dbc.execute(m.payment.delete().where(m.payment.c.debt_id == d.id))
                        payments = json.loads(f.read())
                        for p in payments:
                            dt_str = payments[p]["month"]
                            money = payments[p]["summ"]
                            dt = datetime.datetime.strptime(f"{dt_str}-01", "%Y-%m-%d").date()
                            await dbc.execute(
                                m.payment.insert().values(
                                    debt_id=d.id,
                                    date=dt,
                                    amount=int(money),
                                    author_email=d.author_email,
                                )
                            )
                except Exception as e:
                    print(e)
        await self.dbe.dispose()


async def main():
    worker = ImportData(dbe)
    await worker.run()
    return


asyncio.run(main())
