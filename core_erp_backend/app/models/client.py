from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.master import State, City

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    address = Column(Text)
    state_id = Column(Integer, ForeignKey("states.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    state_rel = relationship("State", back_populates="clients")
    city_rel = relationship("City", back_populates="clients")
    projects = relationship("Project", back_populates="client")