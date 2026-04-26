from pydantic import BaseModel, Field
from models.equipment_type import EquipmentTypes

class Equipment(BaseModel):

    id_equipment: int = Field(...)
    name: str = Field(...)
    category: EquipmentTypes = Field(...)
    description: str = Field(...)

class EquipmentId(Equipment):
    id_gym: int = Field(...)