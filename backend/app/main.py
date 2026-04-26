from fastapi import FastAPI
from models.gimnasio import GimnasioEntrada, GimnasioSalida
from middlewares.ids_middlewares import put_id_gym_equipment
from CSVoperations.create_gym import create_gym
from CSVoperations.create_equipment import create_equipment
from CSVoperations.create_all_models import create_all_models

app = FastAPI(lifespan=create_all_models)

databse = []
@app.get("/")
async def root():
    return {"Hello": "Welcome to CSV prototype of gym app"}

@app.get("/gimnasio")
async def gimnasio_get():
    return databse
@app.post("/gimnasio",response_model=GimnasioSalida)
async def gimnasio_post(gimnasio: GimnasioEntrada):
    gimnasioSalida = put_id_gym_equipment(gimnasio)
    create_gym(gimnasioSalida)
    create_equipment(gimnasioSalida.equipment)
    return gimnasioSalida