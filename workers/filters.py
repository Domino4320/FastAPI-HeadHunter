from core.utils import Specialization, City, Status
from typing import Any
import operator


class Filter:
    OPERATORS = {
        "==" : operator.eq,
        ">" : operator.gt,
        "<" : operator.lt,
        ">=" : operator.ge,
        "<=" : operator.le,
        "!=" : operator.ne,
        "like" : lambda item, value: item.like(f"%{value}%")
    }
    def __init__(self, value : Any, name : str, model : Any, operator : str):
        self.value = value
        self.name = name
        self.model = model
        self.operator = operator
        if (operator not in Filter.OPERATORS):
            raise ValueError("Undefined operator")

    def get_expression(self) -> bool:
        
    


# Реализовать общие фильтры по логическим операциям и именам атрибутов (через магические методы)
# Сделать класс обработчик фильтров
