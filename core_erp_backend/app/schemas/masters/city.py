from pydantic import BaseModel

class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    state_id: int

class CityOut(BaseModel):
    id: int
    name: str
    state_id: int

    class Config:
        from_attributes = True
