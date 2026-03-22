from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Patient

patient_router = APIRouter()

templates = Jinja2Templates(directory="templates")

patients = [
    {"id": 1, "name": "John Doe", "age": 30, "condition": "Flu"},
    {"id": 2, "name": "Jane Smith", "age": 25, "condition": "Cold"}
]

@patient_router.get("/patients/")
async def get_patients():
    return patients

@patient_router.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} was not found"
    )

@patient_router.post("/patients/")
async def create_patient(patient: Patient):
    patients.append(patient.dict())
    return patient

@patient_router.put("/patients/{patient_id}")
async def update_patient(patient_id: int, updated_patient: Patient):
    for index, patient in enumerate(patients):
        if patient["id"] == patient_id:
            patients[index] = updated_patient.dict()
            return updated_patient
    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} was not found"
    )

@patient_router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    for index, patient in enumerate(patients):
        if patient["id"] == patient_id:
            deleted = patients.pop(index)
            return deleted
    raise HTTPException(
        status_code=404,
        detail=f"Patient with ID {patient_id} was not found"
    )

@patient_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "patients": patients
    })

@patient_router.get("/patient/{id}", response_class=HTMLResponse)
async def get_patient_page(request: Request, id: int):
    for patient in patients:
        if patient["id"] == id:
            return templates.TemplateResponse("patient.html", {
                "request": request,
                "patient": patient
            })
    raise HTTPException(status_code=404, detail="Patient not found")