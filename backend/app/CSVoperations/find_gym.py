import pandas as pd

def find_gym_id(id: int):

    dataFrame = pd.read_csv('gimnasios.csv')
    filtrado = dataFrame[dataFrame['id_gimnasio'] == id]

    if filtrado.empty:
        return {"Error":"No Existe este gimnasio"}
    else:
        return filtrado.iloc[0].to_dict()