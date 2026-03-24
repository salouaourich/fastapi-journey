from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Patient
from database import managed_db

patient_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@patient_router.get("/patients/")
async def get_patients():
    with managed_db() as db:
        return db.get_all()


@patient_router.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    with managed_db() as db:
        patient = db.get(patient_id)
    if patient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} was not found"
        )
    return patient


@patient_router.post("/patients/")
async def create_patient(patient: Patient):
    with managed_db() as db:
        new_id = db.create(patient)
        return db.get(new_id)


@patient_router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, updated_patient: Patient):
    with managed_db() as db:
        patient = db.get(patient_id)
        if patient is None:
            raise HTTPException(
                status_code=404,
                detail=f"Patient with ID {patient_id} was not found"
            )
        return db.update(patient_id, updated_patient)


@patient_router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    with managed_db() as db:
        patient = db.get(patient_id)
        if patient is None:
            raise HTTPException(
                status_code=404,
                detail=f"Patient with ID {patient_id} was not found"
            )
        db.delete(patient_id)
        return patient


@patient_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    with managed_db() as db:
        patients = db.get_all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "patients": patients
    })


@patient_router.get("/patient/{id}", response_class=HTMLResponse)
async def get_patient_page(request: Request, id: int):
    with managed_db() as db:
        patient = db.get(id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return templates.TemplateResponse("patient.html", {
        "request": request,
        "patient": patient
    })