from dataclasses import field

from sqlmodel import SQLModel, Field
from models.equipmentTypes import EquipmentTypes

class Equipment(SQLModel):
    id_location: int = Field(foreign_key = "locationid.id_location")
    name: str = Field(...)
    category: EquipmentTypes = Field(...)
    photo_url: str = Field(...)
    description: str = Field(...)

class EquipmentId(Equipment, table=True):
    id_equipment: int | None = Field(default=None, primary_key=True)