from sqlmodel import SQLModel, Field
from models.GymTypes import GymTypes

class Location(SQLModel, table=True):

    id_location: int | None = Field(default = None, primary_key=True)
    id_company: int = Field(foreign_key="company.id_company")
    address: str = Field(...)
    type_gym: GymTypes = Field(...)
    #services: list[str] = []
    pool: bool = False
    pool_number: int = 0
    boxing_ring: bool = False
    boxing_ring_number: int = 0
