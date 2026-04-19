from sqlmodel import Session, create_engine, SQLModel
from fastapi import FastAPI, Depends
from typing import Annotated

sql_name = "gymapp.db" #nombre de base de datos
sql_url = f"sqlite:///{sql_name}" # la url simplemente es sqlite:/// y el nombre de base de datos

engine = create_engine(sql_url) # El motor es creada por la funcuon create_engine y como parametro recibe la url esplicada arriba

def create_all_tables(app: FastAPI): # Funcion que crea todas las tablas antes de que inicie la app
    SQLModel.metadata.create_all(engine)
    yield

def get_session() -> Session: # Cada vez que se llama en endpoint se genera una sesion o conversacion temporal mientras dura el endpoint
    with Session(engine) as session:
        yield session

Conversation = Annotated[Session, Depends(get_session)] # con esto evitamos poner en cada endpoint lo que esta dentro de Annotated