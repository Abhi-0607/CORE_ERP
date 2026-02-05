from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.masters.location import (
    get_all_states,
    get_cities_by_state,
    get_states,
    get_state_by_id,
    get_state_by_name,
    create_state,
    delete_state,
)
from app.schemas.masters.state import StateOut, StateCreate
from app.schemas.masters.city import (
    CityOut,
    CityCreate,
)

router = APIRouter(prefix="/masters/location", tags=["Masters - Location"])

@router.get("/states", response_model=list[StateOut])
def list_states(db: Session = Depends(get_db)):
    return get_all_states(db)

@router.get("/cities", response_model=list[CityOut])
def list_cities(state_id: int, db: Session = Depends(get_db)):
    return get_cities_by_state(db, state_id)
