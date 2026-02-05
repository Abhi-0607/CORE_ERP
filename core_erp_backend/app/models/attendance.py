from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models import Employee
from datetime import datetime



class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    year = Column(Integer)
    month = Column(Integer)
    attendance_data = Column(JSON)  # Store attendance matrix
    loss_of_pay = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    employee = relationship("Employee", back_populates="attendances")
    
    __table_args__ = (UniqueConstraint('employee_id', 'year', 'month', name='unique_employee_month_year'),)