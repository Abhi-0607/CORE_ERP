from sqlalchemy.orm import Session
from app.models.masters.state import State
from app.models.masters.city import City
from app.schemas.masters.state import StateOut, StateCreate
from app.schemas.masters.city import CityOut, CityCreate

def get_all_states(db: Session):
    return db.query(State).order_by(State.name.asc()).all()

def get_cities_by_state(db: Session, state_id: int):
    return (
        db.query(City)
        .filter(City.state_id == state_id)
        .order_by(City.name.asc())
        .all()
    )

# -------------------
# STATES CRUD
# -------------------

def get_states(db: Session):
    return db.query(State).order_by(State.name.asc()).all()


def get_state_by_id(db: Session, state_id: int):
    return db.query(State).filter(State.id == state_id).first()


def get_state_by_name(db: Session, name: str):
    return db.query(State).filter(State.name == name).first()


def create_state(db: Session, state_in: StateCreate):
    existing = get_state_by_name(db, state_in.name)
    if existing:
        return existing

    state = State(name=state_in.name)
    db.add(state)
    db.commit()
    db.refresh(state)
    return state


def delete_state(db: Session, state_id: int):
    state = get_state_by_id(db, state_id)
    if not state:
        return None

    db.delete(state)
    db.commit()
    return state


# -------------------
# CITIES CRUD
# -------------------

def get_cities_by_state(db: Session, state_id: int):
    return (
        db.query(City)
        .filter(City.state_id == state_id)
        .order_by(City.name.asc())
        .all()
    )


def get_city_by_id(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def create_city(db: Session, city_in: CityCreate):
    # prevent duplicates within same state
    existing = (
        db.query(City)
        .filter(City.state_id == city_in.state_id, City.name == city_in.name)
        .first()
    )
    if existing:
        return existing

    city = City(name=city_in.name, state_id=city_in.state_id)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = get_city_by_id(db, city_id)
    if not city:
        return None

    db.delete(city)
    db.commit()
    return city
