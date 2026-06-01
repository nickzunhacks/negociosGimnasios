from sqlmodel import Session, create_engine, SQLModel
from fastapi import FastAPI, Depends
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv() # Carga las variables de entorno puestas en el .env

SQLITE_URL = os.getenv("sqlite") # Variable de entorno para crecenciales sensibles

engine = create_engine(SQLITE_URL) # El motor es creada por la funcuon create_engine y como parametro recibe la url esplicada arriba

def create_all_tables(app: FastAPI): # Funcion que crea todas las tablas antes de que inicie la app
    SQLModel.metadata.create_all(engine)
    yield

def get_session() -> Session: # Cada vez que se llama en endpoint se genera una sesion o conversacion temporal mientras dura el endpoint
    with Session(engine) as session:
        yield session

Conversation = Annotated[Session, Depends(get_session)] # con esto evitamos poner en cada endpoint lo que esta dentro de Annotated