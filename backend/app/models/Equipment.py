from dataclasses import field

from sqlmodel import SQLModel, Field
from models.EquipmentTypes import EquipmentTypes

class Equipment(SQLModel, table=True):

    id_equipment: int | None = Field(default = None, primary_key = True)
    id_location: int = Field(foreign_key = "location.id_location")
    name: str = Field(...)
    category: EquipmentTypes = Field(...)
    photo_url: str = Field(...)
    description: str = Field(...)