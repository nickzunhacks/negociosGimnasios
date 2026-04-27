import csv
from models.gimnasio import GimnasioEntrada, GimnasioSalida
import pandas as pd

def new_gym_id() -> int:

    dataFrame = pd.read_csv('gimnasios.csv')
    max_id = dataFrame['id_gimnasio'].max()

    if pd.isna(max_id):
        return 1

    return max_id+1

def create_gym(gimnasio: GimnasioEntrada):

    new_id = new_gym_id()
    print(new_id)
    gimnasioSalida = GimnasioSalida(id_gimnasio=new_id,**gimnasio.model_dump())

    with open("gimnasios.csv",'a',newline='') as file:
        columnas = gimnasioSalida.model_dump().keys()
        writer = csv.DictWriter(file, fieldnames=columnas)
        writer.writerow(gimnasioSalida.model_dump())

    return gimnasioSalida
