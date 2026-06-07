from sqlmodel import SQLModel, Field

class Company(SQLModel):
        id_owner: int = Field(foreign_key = "ownerid.id_owner")
        name: str = Field(...)
        logoUrl: str = Field(...)
        phone: str = Field(...)
        email: str = Field(...)

class CompanyId(Company, table=True):
    id_company: int | None = Field(default=None, primary_key=True)

class CompanyUpdate(SQLModel):
        name: str | None = None
        phone: str | None = None
        email: str | None = None
        logoUrl: str | None = None