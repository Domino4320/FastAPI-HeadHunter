from typing import Any
from fastapi import HTTPException, status
import re
from enum import Enum
from abc import ABC, abstractmethod
from pwdlib import PasswordHash


def check_changes_availability(object) -> Any:
    if not object.model_dump(exclude_unset=True):
        raise ValueError("Хотя бы одно значение должно меняться обязательно")
    return object


class ResultCheck:

    @staticmethod
    def check_result(result: list, detail: str) -> None:
        if bool(result) == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class RegexBuilder:
    def __init__(self):
        self._uppers = False
        self._lowers = False
        self._special_symbols = ""
        self._numbers = False
        self._lowers_rus = False
        self._uppers_rus = False

    def add_uppers(self):
        self._uppers = True
        return self

    def add_lowers(self):
        self._lowers = True
        return self

    def add_special_symbols(self, special_symbols: str = "!#$%&*_-"):
        self._special_symbols = special_symbols
        return self

    def add_numbers(self):
        self._numbers = True
        return self

    def add_lowers_rus(self):
        self._lowers_rus = True
        return self

    def add_uppers_rus(self):
        self._uppers_rus = True
        return self

    def build(self):
        inner_pattern_list = [
            "a-z" if self._lowers else "",
            "A-Z" if self._uppers else "",
            "0-9" if self._numbers else "",
            "а-я" if self._lowers_rus else "",
            "А-Я" if self._uppers_rus else "",
            self._special_symbols,
        ]
        inner_pattern = "".join(inner_pattern_list)
        full_pattern = rf"^[{inner_pattern}]+$"
        return full_pattern


class SymbolsValidator:

    @staticmethod
    def validate_on_correct_symbols(string: str, regex: str) -> bool:
        return bool(re.search(rf"{regex}", string))

    @staticmethod
    def validate_on_upper_symbol_availability(string: str) -> bool:
        return bool(re.search(r"[A-Z]", string))

    @staticmethod
    def validate_on_lower_symbol_availability(string: str) -> bool:
        return bool(re.search(r"[a-z]", string))

    @staticmethod
    def validate_on_special_symbol_availability(string: str) -> bool:
        return bool(re.search(r"[!#$%&*_-]", string))

    @staticmethod
    def validate_on_number_availability(string: str) -> bool:
        return bool(re.search(r"[0-9]", string))


class ValidationProxy:
    @staticmethod
    def validate(
        method_name: str,
        exc_message: str,
        *,
        exception: type[Exception] = ValueError,
        validator=SymbolsValidator,
        method_args: list | None = None,
    ):
        validation_method = getattr(validator, method_name)
        if validation_method(*(method_args or [])):
            return True
        raise exception(exc_message)


class ValidationStrategy(ABC):

    @classmethod
    @abstractmethod
    def validate():
        pass


class LoginValidationStrategy(ValidationStrategy):

    @staticmethod
    def validate(string: str):
        ValidationProxy.validate(
            "validate_on_correct_symbols",
            "Login contain`s not allowed symbols",
            method_args=[
                string,
                RegexBuilder()
                .add_lowers()
                .add_numbers()
                .add_special_symbols("_")
                .add_uppers()
                .build(),
            ],
        )


class PasswordValidationStrategy(ValidationStrategy):

    @staticmethod
    def validate(string: str):
        ValidationProxy.validate(
            "validate_on_correct_symbols",
            "Password contain`s not allowed symbols",
            method_args=[
                string,
                RegexBuilder()
                .add_lowers()
                .add_numbers()
                .add_special_symbols()
                .add_uppers()
                .build(),
            ],
        )
        ValidationProxy.validate(
            "validate_on_upper_symbol_availability",
            "Password must contain`s one or more symbol in upper case",
            method_args=[string],
        )
        ValidationProxy.validate(
            "validate_on_special_symbol_availability",
            "Password must contain`s one or more special symbol",
            method_args=[string],
        )
        ValidationProxy.validate(
            "validate_on_lower_symbol_availability",
            "Password must contain`s one or more symbol in lower case",
            method_args=[string],
        )
        ValidationProxy.validate(
            "validate_on_number_availability",
            "Password must contain`s one or more number",
            method_args=[string],
        )


class Hasher:
    hasher = PasswordHash.recommended()

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.hasher.hash(password)

    @classmethod
    def verify_password(cls, password, hash):
        return cls.hasher.verify(password, hash)
