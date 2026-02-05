from pydantic import BaseModel


class StateBase(BaseModel):
    name: str


class StateCreate(StateBase):
    pass

class StateOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
