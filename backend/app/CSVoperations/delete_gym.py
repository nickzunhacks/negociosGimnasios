import pandas as pd
from CSVoperations.find_gym import find_gym_id

def delete_gym(id:int):

    gym = find_gym_id(id)

    if "Error" in gym:
        return {"Error": "Gimnasio no encontrado"}

    dataFrame = pd.read_csv('gimnasios.csv')
    gimnasio = dataFrame.loc[dataFrame['id_gimnasio'] == id, 'activo'] = False
    dataFrame.to_csv('gimnasios.csv',index=False)

    delete_equipment_related(id)

    return {"Exito":"Gimnasio eliminado correctamente"}

def delete_equipment_related(id:int):

    dataFrame = pd.read_csv('equipment.csv')
    dataFrame.loc[ (dataFrame['id_gym'] == id) & (dataFrame['activo'] == True), 'activo' ] = False
    dataFrame.to_csv('equipment.csv', index=False)

