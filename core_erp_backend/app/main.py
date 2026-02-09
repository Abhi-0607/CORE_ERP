from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth
from app.routers.masters import location
from fastapi.middleware.cors import CORSMiddleware

#forms imports
from app.models.employees.employee_registration import Employee
from app.routers.employees import employee_registration
#from app.schemas.employees.employee_registration import Employee


app = FastAPI(title="Core ERP Backend")

# CORS SETTINGS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS, etc
    allow_headers=["*"],   # allow Authorization, Content-Type, etc
)


app.include_router(auth.router)
app.include_router(location.router)
app.include_router(employee_registration.router)
