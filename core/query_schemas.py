from pydantic import BaseModel, model_validator, PrivateAttr, Field, field_validator
from fastapi import HTTPException, status
from typing import Self


class RangeValuesSchema(BaseModel):

    min: int | None = None
    max: int | None = None
    _is_nullable: bool = PrivateAttr(default=False)

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.model_dump(exclude_none=True):
            self._is_nullable = True
            return self
        if self.max > self.min:
            return self
        raise ValueError(
            "Max less or equal then min",
        )


class PositiveRangeValuesSchema(RangeValuesSchema):
    @model_validator(mode="after")
    def check_positive(self) -> Self:
        if not self._is_nullable:
            if self.min >= 0 and self.max >= 0:
                return self
            raise ValueError("min and max values must be positive")


class KeywordSchema(BaseModel):
    keyword: str | None = Field(None, min_length=1, max_length=200)

    @field_validator("keyword", mode="before")
    @classmethod
    def validate_keyword(cls, keyword):
        if isinstance(keyword, str):
            return keyword.strip()
        return keyword
