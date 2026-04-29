from fastapi import FastAPI
from models.equipment import EquipmentId,Equipment
from models.gimnasio import GimnasioEntrada, GimnasioSalida, TiposGimnasios
from models.company import CompanySalida, CompanyEntrada
from CSVoperations.create_gym import create_gym
from CSVoperations.create_equipment import create_equipment_id
from CSVoperations.create_all_models import create_all_models
from CSVoperations.find_equipment import find_equipment_id_gym, find_one_equipment
from CSVoperations.find_gym import find_gym_id, find_gym_id_company, find_gyms_category
from CSVoperations.create_company import new_company_salida
from CSVoperations.find_company import find_company_id
from CSVoperations.delete_equipment import delete_equipment
from CSVoperations.delete_gym import delete_gym
from CSVoperations.delete_company import delete_company
from CSVoperations.mod_company import edit_name
from CSVoperations.mod_gym import edit_name_gym
from CSVoperations.mod_equipment import edit_description_equipment
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

@app.get(f"/equipment/{id}")
async def equipment_get(id: int):
    return find_one_equipment(id)

@app.get(f"/gyms-of-company/{id}")
async def get_gyms_of_company(id: int):
    return find_gym_id_company(id)
@app.get(f"/equipment-of-gym/{id}")
async def get_equipment_of_gym(id: int):
    return find_equipment_id_gym(id)

@app.get(f'/gym-category/{type}')
async def get_gym_category(type: TiposGimnasios):
    return find_gyms_category(type)

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

@app.patch("/name-company/{name}/{id}")
def edit_name_company(name: str, id: int):
    return edit_name(name, id)

@app.patch("/name-gym/{name}/{id}")
def edit_name_company(name: str, id: int):
    return edit_name_gym(name, id)

@app.patch("/description-equipment/{description}/{id}")
def edit_name_company(description: str, id: int):
    return edit_description_equipment(description, id)
@app.delete(f"/equipment/{id}")
async def equipment_delete(id: int):
    return delete_equipment(id)

@app.delete(f"/gimnasio/{id}")
async def gimnasio_delete(id: int):
    return delete_gym(id)

@app.delete(f"/company/{id}")
async def company_delete(id: int):
    return delete_company(id)