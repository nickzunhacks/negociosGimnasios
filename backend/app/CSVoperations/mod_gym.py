import pandas as pd
from CSVoperations.find_gym import find_gym_id

def edit_name_gym(name: str, id: int):

    gym = find_gym_id(id)

    if "Error" in gym:
        return {"Error": "Este gimnasio no existe"}

    dataFrame = pd.read_csv("gimnasios.csv")
    dataFrame.loc[dataFrame['id_gimnasio'] == id, 'name'] = name
    dataFrame.to_csv("gimnasios.csv", index=False)

    updated_gym = dataFrame[dataFrame['id_gimnasio'] == id].iloc[0]

    return updated_gym.to_dict()