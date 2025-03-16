import asyncio
import datetime
import json
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from db import dbe
import models as m


async def run(dbe: AsyncEngine):
    async with dbe.begin() as dbc:
        query = (
            sa.select(
                m.debt.c.id,
                m.user.c.email.label("author_email"),
            )
            .select_from(m.debt)
            .order_by(m.debt.c.date)
        )
        query = query.where(m.user.c.email == m.debt.c.author_email)
        res = await dbc.execute(query)
        debts = res.fetchall()
        for debt in debts:
            try:
                with open(f"data/{debt.id}.json", mode="r") as f:
                    await dbc.execute(m.payment.delete().where(m.payment.c.debt_id == debt.id))
                    payments = json.loads(f.read())
                    for payment in payments:
                        dt_str = payments[payment]["month"]
                        money = payments[payment]["summ"]
                        dt = datetime.datetime.strptime(f"{dt_str}-01", "%Y-%m-%d").date()
                        await dbc.execute(
                            m.payment.insert().values(
                                debt_id=debt.id,
                                date=dt,
                                amount=int(money),
                                month=dt_str,
                                author_email=debt.author_email,
                            )
                        )
            except Exception as e:
                print(e)
    await dbe.dispose()


async def main():
    await run(dbe)
    return


asyncio.run(main())
