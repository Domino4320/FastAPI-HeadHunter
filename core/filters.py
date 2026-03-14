from core.utils import Specialization, City, Status
from typing import Any
from sqlalchemy import and_, BinaryExpression, Column
from abc import ABC, abstractmethod


class Filter(ABC):
    """
    Абстрактный класс для фильтров
    """

    def __init__(self, column_name: str, model: Any):
        self.column_name = column_name
        self.model = model

    @abstractmethod
    def get_expression(self) -> BinaryExpression:
        column: Column = getattr(self.model, self.column_name)
        return column


class RangeFilter(Filter):
    def __init__(self, column_name: str, model: Any, min: int, max: int):
        """
        фильтр для поиска значений с диапазоном между min и max
        """
        super().__init__(column_name, model)
        self.min = min
        self.max = max

    def get_expression(self) -> BinaryExpression:
        column = super().get_expression()
        return and_(
            column >= self.min,
            column <= self.max,
        )


class LikeFilter(Filter):
    def __init__(self, column_name, model, value):
        """
        фильтр для поиска значений, содержащих value
        """
        super().__init__(column_name, model)
        self.value = value

    def get_expression(self) -> BinaryExpression:
        column = super().get_expression()
        return column.ilike(f"%{self.value}%")


class EqualFilter(Filter):
    """
    фильтр для проверки соответствия значения value
    """

    def __init__(self, column_name, model, value):
        super().__init__(column_name, model)
        self.value = value

    def get_expression(self) -> BinaryExpression:
        column = super().get_expression()
        return column == self.value


class FilterCollection:
    def __init__(self, *filters: Filter):
        self.filters: list[Filter] = []
        for arg in filters:
            if isinstance(arg, filter):
                self.filters.append(arg)
            else:
                raise ValueError("FilterCollection can includes only Filter objects")

    def __iter__(self):
        for filter in self.filters:
            yield filter

    def get_full_expression(self):
        return and_(*self)


# Реализовать общие фильтры по логическим операциям и именам атрибутов (через магические методы)
# Сделать класс обработчик фильтров
