from sqlmodel import SQLModel, Field

class Company(SQLModel, table=True):

    id_company: int = Field(primary_key=True)
    id_owner: int = Field(...)
    name: str = Field(...)
    logoUrl: str = Field(...)
    phone: str = Field(...)
    email: str = Field(...)
    multiLocation: bool = Field(...)
