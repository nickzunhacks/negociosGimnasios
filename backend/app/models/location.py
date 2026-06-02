from sqlmodel import SQLModel, Field
from models.gymTypes import GymTypes
from fastapi import UploadFile

class Location(SQLModel):

    id_company: int = Field(foreign_key="companyid.id_company")
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)
    address: str = Field(...)
    type_gym: GymTypes = Field(...)
    pool: bool = False
    pool_number: int = 0
    boxing_ring: bool = False
    boxing_ring_number: int = 0
    photo_url: str | None = Field(default=None)

class LocationId(Location, table=True):
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    id_location: int | None = Field(default=None, primary_key=True)