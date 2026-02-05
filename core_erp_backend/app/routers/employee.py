from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app import crud, models
from app import schemas
from app.database import get_db
from app.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_model=List[schemas.Employee])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    department_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.employee_models.User = Depends(get_current_user)
):
    """
    Get employees with optional filtering.
    HR/Admin: All employees
    Manager: Employees in their department
    Employee: Only themselves
    """
    if current_user.role in ["HR", "Admin"]:
        query = db.query(models.employee_models.Employee)
        
        if department_id:
            query = query.filter(models.employee_models.Employee.department_id == department_id)
        
        if status:
            query = query.filter(models.employee_models.Employee.status == status)
        
        employees = query.offset(skip).limit(limit).all()
        
    elif current_user.role == "Manager":
        # Get manager's department from their employee record
        if not current_user.employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Manager must be linked to an employee"
            )
        
        manager = crud.employee.get(db, id=current_user.employee_id)
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager employee record not found"
            )
        
        employees = crud.employee.get_multi_by_department(
            db, department_id=manager.department_id, skip=skip, limit=limit
        )
    
    else:  # Employee
        if not current_user.employee_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee record not found"
            )
        
        employee = crud.employee.get(db, id=current_user.employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee record not found"
            )
        
        employees = [employee]
    
    return employees

@router.post("/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_in: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.employee_models.User = Depends(require_roles(["HR", "Admin"]))
):
    """
    Create new employee. Only HR and Admin can create employees.
    """
    # Check if employee_id already exists
    employee = crud.employee.get_by_employee_id(db, employee_id=employee_in.employee_id)
    if employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    # Check if email already exists
    employee = crud.employee.get_by_email(db, email=employee_in.personal_email)
    if employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if Aadhar already exists
    employee = crud.employee.get_by_aadhar(db, aadhar_no=employee_in.aadhar_no)
    if employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aadhar number already registered"
        )
    
    # Create employee
    employee = crud.employee.create(db, obj_in=employee_in)
    return employee

@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.employee_models.User = Depends(get_current_user)
):
    """
    Get employee by ID with role-based access control.
    """
    employee = crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check permissions
    if current_user.role in ["HR", "Admin"]:
        pass  # HR and Admin can view all
    elif current_user.role == "Manager":
        # Manager can only view employees in their department
        manager = crud.employee.get(db, id=current_user.employee_id)
        if not manager or manager.department_id != employee.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this employee"
            )
    else:  # Employee
        # Employee can only view themselves
        if current_user.employee_id != employee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this employee"
            )
    
    return employee

@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: models.employee_models.User = Depends(require_roles(["HR", "Admin"]))
):
    """
    Update employee. Only HR and Admin can update employees.
    """
    employee = crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    employee = crud.employee.update(db, db_obj=employee, obj_in=employee_in)
    return employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.employee_models.User = Depends(require_roles(["HR", "Admin"]))
):
    """
    Delete employee. Only HR and Admin can delete employees.
    """
    employee = crud.employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    crud.employee.remove(db, id=employee_id)
    return None