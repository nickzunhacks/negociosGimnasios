import csv
import pandas as pd
from models.equipment import EquipmentId, Equipment

def create_equipment(equipment: list[EquipmentId]):

    with open('equipment.csv', 'a', newline='') as file:

        columnas = equipment[0].model_dump().keys()
        writer = csv.DictWriter(file,fieldnames=columnas)

        for i in equipment:
            writer.writerow(i.model_dump())

def new_id_company():
    dataFrame = pd.read_csv('equipment.csv')
    max_id = dataFrame['id_equipment'].max()

    if pd.isna(max_id):
        return 1

    return max_id+1

def create_equipment_id(equipment: Equipment):
    id = new_id_company()
    newEquipment = EquipmentId(**equipment.model_dump(),id_equipment=id)
    with open('equipment.csv', 'a', newline='') as file:
        columnas = newEquipment.model_dump().keys()
        writer = csv.DictWriter(file,fieldnames=columnas)
        writer.writerow(newEquipment.model_dump())
    return  newEquipment