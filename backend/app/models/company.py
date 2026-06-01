from sqlmodel import SQLModel, Field

class Company(SQLModel):
    id_owner: int = Field(...)
    name: str = Field(...)
    logoUrl: str = Field(...)
    phone: str = Field(...)
    email: str = Field(...)
    multiLocation: bool = Field(...)

class CompanyId(Company, table=True):
    id_company: int | None = Field(default=None, primary_key=True)