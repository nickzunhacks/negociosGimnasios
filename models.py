from pydantic import BaseModel, Field
from tipos_gimnasio import TiposGimnasios

class Gimnasio(BaseModel):

    Name: str = Field(..., max_length= 64)
    typeGym: TiposGimnasios = Field(...)
    multilocation: bool = False
    locationNumber: int = 1
    cardiovascularMachines: list[str] = []
    strengthMachines: list[str] = []
    dumbells: list[str] = []
    benches: list[str] = []
    elasticBands: list[str] = []
    services: list[str] = []
    otherEquipment: list[str] = []
    pool: bool = False
    poolNumber: int = 0
    boxingRing: bool = False
    boxingRingNumber: int = 0

gimansio1 = Gimnasio(Name="be fit gym", typeGym=TiposGimnasios.TRADICIONAL)

print(gimansio1)