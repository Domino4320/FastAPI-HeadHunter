from typing import Self, Any
from fastapi import HTTPException, status


def check_changes_availability(object) -> Any:
    if not object.model_dump(exclude_unset=True):
        raise ValueError("Хотя бы одно значение должно меняться обязательно")
    return object


class ResultCheck:

    @staticmethod
    def check_result(result: list, detail: str) -> None:
        if bool(result) == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
