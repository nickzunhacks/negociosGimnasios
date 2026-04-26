import csv
from models.equipment import EquipmentId

def create_equipment(equipment: list[EquipmentId]):

    with open('equipment.csv', 'a', newline='') as file:

        columnas = equipment[0].model_dump().keys()
        writer = csv.DictWriter(file,fieldnames=columnas)

        for i in equipment:
            writer.writerow(i.model_dump())