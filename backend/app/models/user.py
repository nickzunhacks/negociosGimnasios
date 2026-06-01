from matplotlib.table import table
from pycparser.c_ast import Default
from sqlmodel import SQLModel, Field

class User(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    edad: int = Field(gt=11, lt=100)
    username: str = Field(...)
    password: str = Field(min_length=5, max_length=30)
    rol: str = Field(default="deportista")

class UserId(User, table=True):
    id: int | None = Field(default=None, gt=0, primary_key=True)