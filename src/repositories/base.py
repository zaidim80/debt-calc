from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa

from errors import NotFound

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: sa.Table, schema_cls: Type[T]):
        self.model = model
        self.schema_cls = schema_cls

    async def _execute_query(self, dbc: AsyncConnection, query: sa.Select):
        """Выполнение запроса с возвратом результата"""
        res = await dbc.execute(query)
        return res

    def _build_select_query(self, *columns) -> sa.Select:
        """Построение базового SELECT запроса"""
        return sa.select(*columns)

    def _build_insert_query(self, values: dict) -> sa.Insert:
        """Построение INSERT запроса"""
        return sa.insert(self.model).values(**values)

    def _build_update_query(self, where_clause: sa.ClauseElement, values: dict) -> sa.Update:
        """Построение UPDATE запроса"""
        return sa.update(self.model).where(where_clause).values(**values)

    def _build_delete_query(self, where_clause: sa.ClauseElement) -> sa.Delete:
        """Построение DELETE запроса"""
        return sa.delete(self.model).where(where_clause)

    async def get_by_id(self, dbc: AsyncConnection, id_value: int) -> T:
        """Получение записи по ID"""
        query = self._build_select_query(self.model).where(self.model.c.id == id_value)
        result = await self._execute_query(dbc, query)
        item = result.first()
        if not item:
            raise NotFound(f"Запись с id={id_value} не найдена")
        return self.schema_cls.model_validate(item, from_attributes=True) 