from pydantic import BaseModel, model_validator
from fastapi import Depends, HTTPException, status


class RangeValuesSchema(BaseModel):

    min: int | None = None
    max: int | None = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.model_dump(exclude_unset=True) and max > min:
            return self
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request doesn't includes min or max values or max less or equal then min",
        )
