from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


from sqlalchemy.sql import func
from app.database import Base

# Performance Appraisal
class PerformanceAppraisal(Base):
    __tablename__ = "performance_appraisals"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    appraisal_date = Column(Date)
    increment_amount = Column(Float)
    promotion = Column(Boolean, default=False)
    promoted_from_id = Column(Integer, ForeignKey("designations.id"), nullable=True)
    promoted_to_id = Column(Integer, ForeignKey("designations.id"), nullable=True)
    increment_effective_date = Column(Date)
    salary_after_increment = Column(Float)
    performance_appraiser = Column(String(100))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    employee = relationship("Employee", back_populates="performance_appraisals")
    promoted_from = relationship("Designation", foreign_keys=[promoted_from_id])
    promoted_to = relationship("Designation", foreign_keys=[promoted_to_id])