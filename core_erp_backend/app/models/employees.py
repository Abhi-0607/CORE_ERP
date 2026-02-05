from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Date, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# Employee Registration
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    # Personal Details
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100), nullable=True)
    fathers_name = Column(String(100), nullable=True)
    photograph_url = Column(String(500), nullable=True)
    
    # Employment Details
    date_of_joining = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.id"))
    employee_id = Column(String(50), unique=True, index=True)
    
    # Contact Details
    mobile_no = Column(String(15))
    personal_email = Column(String(255))
    
    # Personal Information
    date_of_birth = Column(Date)
    gender = Column(String(10))
    current_location = Column(String(200), nullable=True)
    address = Column(Text)
    city_id = Column(Integer, ForeignKey("cities.id"))
    state_id = Column(Integer, ForeignKey("states.id"))
    aadhar_no = Column(String(12), unique=True)
    aadhar_url = Column(String(500), nullable=True)
    
    # Professional Details
    designation_id = Column(Integer, ForeignKey("designations.id"))
    working_location_id = Column(Integer, ForeignKey("cities.id"))
    status = Column(String(20), default="Active")
    
    # Emergency Contact
    emergency_contact = Column(String(15), nullable=True)
    emergency_relation = Column(String(50), nullable=True)
    
    # Medical Details
    blood_group_id = Column(Integer, ForeignKey("blood_groups.id"), nullable=True)
    
    # Exit Details
    date_of_relieving = Column(Date, nullable=True)
    permanent_address = Column(Text, nullable=True)
    
    # Salary & Banking
    salary_ctc = Column(Float)
    bank_name = Column(String(100), nullable=True)
    bank_account_no = Column(String(50), nullable=True)
    account_name = Column(String(100), nullable=True)
    ifsc_code = Column(String(11), nullable=True)
    pan_no = Column(String(10), nullable=True)
    pf_no = Column(String(50), nullable=True)
    esi_no = Column(String(50), nullable=True)
    
    # Education Details
    resume_url = Column(String(500), nullable=True)
    qualification_id = Column(Integer, ForeignKey("qualifications.id"), nullable=True)
    year_of_passing = Column(Date, nullable=True)
    total_experience = Column(Float, nullable=True)
    last_company = Column(String(200), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    city_rel = relationship("City", foreign_keys=[city_id], back_populates="employees")
    state_rel = relationship("State", foreign_keys=[state_id], back_populates="employees")
    working_location = relationship("City", foreign_keys=[working_location_id])
    blood_group = relationship("BloodGroup", back_populates="employees")
    qualification = relationship("Qualification", back_populates="employees")
    user = relationship("User", back_populates="employee", uselist=False)
    
    # Form Relationships
    performance_appraisals = relationship("PerformanceAppraisal", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")
    onsite_travels = relationship("OnsiteTravel", back_populates="employee")
    assets = relationship("EmployeeAsset", back_populates="employee")


class OnsiteTravel(Base):
    __tablename__ = "onsite_travels"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date_of_reaching = Column(Date)
    site_name = Column(String(100))
    project_id = Column(Integer, ForeignKey("projects.id"))
    date_of_return = Column(Date)
    days_of_stay = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    employee = relationship("Employee", back_populates="onsite_travels")
    project = relationship("Project")

class EmployeeAsset(Base):
    __tablename__ = "employee_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    asset_name = Column(String(100))
    asset_type = Column(String(100))
    asset_sl_no = Column(String(100))
    model_name = Column(String(100))
    date_of_assignment = Column(Date)
    asset_description = Column(Text, nullable=True)
    asset_returned_date = Column(Date, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    employee = relationship("Employee", back_populates="assets")

