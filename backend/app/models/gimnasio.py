from pydantic import BaseModel, Field
from models.tipos_gimnasio import TiposGimnasios
from models.equipment import EquipmentId, Equipment

class GimnasioEntrada(BaseModel):
    id_gimnasio: int = Field(...)
    name: str = Field(..., max_length= 64)
    typeGym: TiposGimnasios = Field(...)
    equipment: list[Equipment] = Field(...)
    multilocation: bool = False
    locationNumber: int = 1
    pool: bool = False
    poolNumber: int = 0
    boxingRing: bool = False
    boxingRingNumber: int = 0

class GimnasioSalida(BaseModel):
    id_gimnasio: int = Field(...)
    name: str = Field(..., max_length=64)
    typeGym: TiposGimnasios = Field(...)
    equipment: list[EquipmentId] = Field(...)
    multilocation: bool = False
    locationNumber: int = 1
    pool: bool = False
    poolNumber: int = 0
    boxingRing: bool = False
    boxingRingNumber: int = 0

"""class GimnasioId(Gimnasio):
    id_gimnasio: int = Field(...)
    esto posteriormente sera parte de GimnasioSalida
"""