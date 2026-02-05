from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)

    # relationship
    state = relationship("State",back_populates="cities")

    __table_args__ = (
        UniqueConstraint("state_id", "name", name="uq_city_state_name"),
    )
