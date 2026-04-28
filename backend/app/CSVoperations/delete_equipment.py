import csv
import pandas as pd
from CSVoperations.find_equipment import find_one_equipment

def delete_equipment(id: int):

    equipamiento = find_one_equipment(id)

    if "Error" in equipamiento:
        return equipamiento

    dataFrame = pd.read_csv('equipment.csv')
    equipment = dataFrame.loc[dataFrame['id_equipment'] == id, 'activo'] = False
    dataFrame.to_csv('equipment.csv', index=False)

    return {"Exito":"Se ha eliminado este equipamento"}