from typing import Self, Any
from fastapi import HTTPException, status
import re
from functools import wraps
from typing import Callable


def check_changes_availability(object) -> Any:
    if not object.model_dump(exclude_unset=True):
        raise ValueError("Хотя бы одно значение должно меняться обязательно")
    return object


class ResultCheck:

    @staticmethod
    def check_result(result: list, detail: str) -> None:
        if bool(result) == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ExceptionAdder:

    def __init__(self, error: type[Exception], message: str):
        self.error = error
        self.message = message

    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not func(*args, **kwargs):
                raise self.error(self.message)
            return True

        return wrapper


class PasswordValidator:

    @staticmethod
    @ExceptionAdder(ValueError, "Password contains not correct symbols")
    def validate_on_correct_symbols(password: str) -> bool:
        return bool(re.search(r"^[a-zA-Z0-9!#$%&*_]+$", password))

    @staticmethod
    @ExceptionAdder(
        ValueError,
        "Password doesn`t contains symbol in upper case. Password is not secure.",
    )
    def validate_on_upper_symbol_availability(password: str) -> bool:
        return bool(re.search(r"[A-Z]", password))

    @staticmethod
    @ExceptionAdder(
        ValueError,
        """Password doesn`t contains special symbol. 
        Password is not secure. Allowed special symbols - !#$%&*_""",
    )
    def validate_on_special_symbol_availability(password: str) -> bool:
        return bool(re.search(r"[!#$%&*_]", password))

    @staticmethod
    @ExceptionAdder(
        ValueError,
        "Password doesn`t contains number. Password is not secure.",
    )
    def validate_on_number_availability(password: str) -> bool:
        return bool(re.search(r"[0-9]", password))

    @classmethod
    def full_validate(cls, password: str, skip: list[str] = None) -> bool:
        skip_list = ["full_validate"]
        if skip:
            skip_list.extend(skip)
        for name in dir(cls):
            if name.startswith("__") or name in skip:
                continue
            if callable(func := getattr(cls, name)):
                func(password)
