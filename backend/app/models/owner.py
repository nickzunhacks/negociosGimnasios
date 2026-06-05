from sqlmodel import SQLModel, Field

class Owner(SQLModel):
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=5, max_length=50)

class OwnerId(Owner, table=True):
    id_owner: int | None = Field(default=None, primary_key=True)