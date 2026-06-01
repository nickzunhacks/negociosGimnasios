from sqlmodel import SQLModel, Field
from models.gymTypes import GymTypes

class Location(SQLModel):

    id_company: int = Field(foreign_key="companyid.id_company")
    address: str = Field(...)
    type_gym: GymTypes = Field(...)
    pool: bool = False
    pool_number: int = 0
    boxing_ring: bool = False
    boxing_ring_number: int = 0

class LocationId(Location, table=True):
    id_location: int | None = Field(default=None, primary_key=True)