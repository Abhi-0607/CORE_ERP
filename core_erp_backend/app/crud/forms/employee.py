from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Employee
from core_erp_backend.app.schemas.schemas import EmployeeCreate, EmployeeUpdate
from app.crud.base import CRUDBase

class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_by_employee_id(self, db: Session, employee_id: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.personal_email == email).first()
    
    def get_by_aadhar(self, db: Session, aadhar_no: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.aadhar_no == aadhar_no).first()
    
    def get_multi_by_department(
        self, db: Session, *, department_id: int, skip: int = 0, limit: int = 100
    ) -> List[Employee]:
        return (
            db.query(Employee)
            .filter(Employee.department_id == department_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_active_employees(self, db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
        return (
            db.query(Employee)
            .filter(Employee.status == "Active")
            .offset(skip)
            .limit(limit)
            .all()
        )

employee = CRUDEmployee(Employee)