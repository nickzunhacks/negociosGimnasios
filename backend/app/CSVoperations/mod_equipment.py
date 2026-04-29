import pandas as pd
from CSVoperations.find_equipment import find_one_equipment

def edit_description_equipment(description: str, id: int):

    equipment = find_one_equipment(id)

    if "Error" in equipment:
        return {"Error": "Este equipamiento no existe"}

    dataFrame = pd.read_csv("equipment.csv")
    dataFrame.loc[dataFrame['id_equipment'] == id, 'name'] = description
    dataFrame.to_csv("equipment.csv", index=False)

    updated_equipment = dataFrame[dataFrame['id_equipment'] == id].iloc[0]

    return updated_equipment.to_dict()