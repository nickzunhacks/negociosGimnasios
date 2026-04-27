from fastapi import FastAPI
from models.equipment import EquipmentId,Equipment
from models.gimnasio import GimnasioEntrada, GimnasioSalida
from models.company import CompanySalida, CompanyEntrada
from CSVoperations.create_gym import create_gym
from CSVoperations.create_equipment import create_equipment_id
from CSVoperations.create_all_models import create_all_models
from CSVoperations.find_equipment import find_quipment_id_gym
from CSVoperations.find_gym import find_gym_id
from CSVoperations.create_company import new_company_salida
from CSVoperations.find_company import find_company_id

app = FastAPI(lifespan=create_all_models)
@app.get("/")
async def root():
    return {"Hello": "Welcome to CSV prototype of gym app"}

@app.get(f'/company/{id}')
async def get_company(id: int):
    return find_company_id(id)
@app.get(f"/gimnasio/{id}")
async def gimnasio_get(id: int):
    return find_gym_id(id)

@app.get(f"/equipment_of_gym/{id}")
async def get_equipment_of_gym(id: int):
    return find_quipment_id_gym(id)

@app.post('/company', response_model=CompanySalida)
async def company_post(company: CompanyEntrada):
    return new_company_salida(company)
@app.post("/gimnasio")
async def gimnasio_post(gimnasio: GimnasioEntrada):
    if "Error" in find_company_id(gimnasio.id_company):
        return {"Error": "Company no existe"}
    return create_gym(gimnasio)

@app.post("/equipment")
async def equipment_post(equipment: Equipment):
    if "Error" in find_gym_id(equipment.id_gym):
        return {"Error": "Gym no existe"}
    return create_equipment_id(equipment)
