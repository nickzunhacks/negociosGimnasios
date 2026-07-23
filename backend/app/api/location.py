from fastapi import APIRouter, HTTPException
from db.db import Conversation
from models.gymTypes import GymTypes
from db.operations_location import show_locations, show_location_category,find_one_location, show_locations_all
from db.operations_equipment import show_equipment_gym

router = APIRouter()

# --------------------------------| GET |--------------------------------

# entrega todos los gimnasios
@router.get("/locations-all")
def get_locations_all(session: Conversation):
    return show_locations_all(session)

# entrega todos los gimnasios por categoria
@router.get("/location-categories")
async def get_location_categories(category: GymTypes, session: Conversation):
    return show_location_category(category, session)

#entrega todas lOS GYMS de una empresa
@router.get("/locations")
def get_locations(id_company: int, session: Conversation):
    return show_locations(session, id_company)

# busca un solo gym por id
@router.get("/location-one")
async def find_location(id_location: int, session: Conversation):
    return find_one_location(session, id_location)

# muestra todo el equipamiento del gimnasio
@router.get("/equipment-location")
async def get_equipment_location(id_location: int, session: Conversation):
    equipment = show_equipment_gym(session, id_location)
    if equipment == None:
        raise HTTPException(status_code=404, detail="No equipment or gym inexistent")
    return equipment