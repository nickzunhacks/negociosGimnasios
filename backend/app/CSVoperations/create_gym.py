import csv
from models.gimnasio import GimnasioSalida

def create_gym(gimnasio: GimnasioSalida):

    with open("gimnasios.csv",'a',newline='') as file:
        columnas = gimnasio.model_dump().keys()
        writer = csv.DictWriter(file, fieldnames=columnas)
        writer.writerow(gimnasio.model_dump())
