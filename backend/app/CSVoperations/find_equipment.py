import pandas as pd
from CSVoperations.find_gym import find_gym_id

def find_equipment_id_gym(id: int):

    if "Error" in find_gym_id(id):
        return {"Error": "Gimnasio no encontrado"}

    dataFrame = pd.read_csv('equipment.csv')
    filtrados = dataFrame[ (dataFrame['id_gym'] == id) & (dataFrame['activo'] == True) ]

    if filtrados.empty:
        return {"Error":"Gimnasio sin equipo agregado"}
    else:
        return filtrados.to_dict(orient='records')

def find_one_equipment(id: int):

    dataFrame = pd.read_csv('equipment.csv')
    equipment = dataFrame[ (dataFrame['id_equipment'] == id) & (dataFrame['activo'] == True)]

    if equipment.empty:
        return {"Error":"equipamiento no encontrado"}
    else:
        return equipment.iloc[0].to_dict()


