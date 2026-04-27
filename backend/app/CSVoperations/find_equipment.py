import pandas as pd
from CSVoperations.find_gym import find_gym_id

def find_quipment_id_gym(id: int):

    if "Error" in find_gym_id(id):
        return {"Error": "Gimnasio no encontrado"}

    dataFrame = pd.read_csv('equipment.csv')
    filtrados = dataFrame[dataFrame['id_gym'] == id]

    if filtrados.empty:
        return {"Error":"Gimnasio sin equipo agregado"}
    else:
        return filtrados.to_dict(orient='records')





