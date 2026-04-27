from pydantic import BaseModel, Field

class CompanyEntrada(BaseModel):
    name: str = Field(...)
    #logoUrl: str = Field(...)
    phone: str = Field(...)
    email: str = Field(...)
    multiLocation: bool = False

class CompanySalida(CompanyEntrada):
    id_company: int = Field(gt=0)