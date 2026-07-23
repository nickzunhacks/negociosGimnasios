from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from db.db import Conversation
from models.equipment import Equipment
from db.operations_equipment import create_equipment

router = APIRouter()

# --------------------------------| GET |--------------------------------

# registra un equipment
@router.post("/equipment")
async def post_equipment(equipment: Equipment, session: Conversation):
    new_equipment = await create_equipment(equipment, session)
    if new_equipment == None:
        raise HTTPException(status_code=404, detail="gimnasio no encontrado")
    return new_equipment