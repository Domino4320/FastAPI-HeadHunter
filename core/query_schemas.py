from pydantic import BaseModel, model_validator
from fastapi import HTTPException, status


class RangeValuesSchema(BaseModel):

    min: int | None = None
    max: int | None = None

    @model_validator(mode="after")
    def validate_fields(self):
        if not self.model_dump(exclude_none=True):
            return self
        if self.max > self.min:
            return self
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Max less or equal then min",
        )
