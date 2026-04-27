from pydantic import BaseModel, Field
from models.tipos_gimnasio import TiposGimnasios
from models.equipment import EquipmentId, Equipment

class GimnasioEntrada(BaseModel):
    id_company: int = Field(gt=0)
    name: str = Field(..., max_length= 64)
    typeGym: TiposGimnasios = Field(...)
    address: str = Field(..., max_length=64)
    city: str = Field(..., max_length=64)
    pool: bool = False
    poolNumber: int = 0
    boxingRing: bool = False
    boxingRingNumber: int = 0

class GimnasioSalida(BaseModel):
    id_gimnasio: int = Field(...)
    id_company: int = Field(gt=0)
    name: str = Field(..., max_length=64)
    typeGym: TiposGimnasios = Field(...)
    address: str = Field(..., max_length=64)
    city: str = Field(..., max_length=64)
    pool: bool = False
    poolNumber: int = 0
    boxingRing: bool = False
    boxingRingNumber: int = 0

"""class GimnasioId(Gimnasio):
    id_gimnasio: int = Field(...)
    esto posteriormente sera parte de GimnasioSalida
"""