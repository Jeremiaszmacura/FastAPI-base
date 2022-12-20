from pydantic import BaseModel, Field
from datetime import datetime


class ReservationBase(BaseModel):
    startsAt: datetime
    endsAt: datetime
    is_active: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "startsAt": "",
                "endsAt": "",
                "is_active": False
            }
        }


class ReservationOut(ReservationBase):
    pass
