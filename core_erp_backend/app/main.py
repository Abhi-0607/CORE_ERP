from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth
from app.routers.masters import location
from fastapi.middleware.cors import CORSMiddleware

#forms imports
from app.routers.employees import employee_registration


app = FastAPI(title="Core ERP Backend")

# CORS SETTINGS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, GET, OPTIONS, etc
    allow_headers=["*"],   # allow Authorization, Content-Type, etc
    expose_headers=["*"],  # expose all headers to the client
)


app.include_router(auth.router)
app.include_router(location.router)
app.include_router(employee_registration.router)
