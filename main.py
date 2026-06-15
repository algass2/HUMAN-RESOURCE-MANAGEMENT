from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models
from routers import auth_router, dept_router, emp_router, leave_router, payroll_router, review_router

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HR Management API",
    description="""
## 🏢 Human Resource Management API

A **FastAPI**-based industry-standard REST API for managing employees, departments,
payroll, leave requests, and performance reviews.

### SDG Alignment

A digital tool to manage fair employment, transparent payroll, and structured
performance reviews — contributing to the formalization of labour practices in Sierra Leone.

### Features
- 🔐 JWT-based Authentication & Authorization (OAuth2)
- 👤 Role-based Access Control (Admin / HR Manager / Employee)
- 🏗️ Department Management
- 👥 Employee Management
- 📋 Leave Request Workflow
- 💰 Payroll Processing (async)
- ⭐ Performance Reviews
- 📖 Swagger UI & ReDoc
""",
    version="1.0.0",
    contact={"name": "HR API Support", "email": "hr@example.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_router)
app.include_router(dept_router)
app.include_router(emp_router)
app.include_router(leave_router)
app.include_router(payroll_router)
app.include_router(review_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the HR Management API 🏢",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
