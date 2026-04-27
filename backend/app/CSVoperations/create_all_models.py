import csv
from models.gimnasio import GimnasioSalida
from models.equipment import EquipmentId
from models.company import CompanySalida
from fastapi import FastAPI
from middlewares.existen_modelos import necesitanCrearse

def create_gimnasios():
    header = GimnasioSalida.model_fields.keys()

    with open("gimnasios.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, header)
        writer.writeheader()

def create_equipment():
    header = EquipmentId.model_fields.keys()

    with open("equipment.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, header)
        writer.writeheader()

def create_companies():
    header = CompanySalida.model_fields.keys()

    with open("companies.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, header)
        writer.writeheader()

def create_all_models(app: FastAPI):

    if necesitanCrearse():
        print("Necesitan cerarse")
        create_gimnasios()
        create_equipment()
        create_companies()
    yield