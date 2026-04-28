import pandas as pd
from CSVoperations.find_company import find_company_id

def find_gym_id(id: int):

    dataFrame = pd.read_csv('gimnasios.csv')
    filtrado = dataFrame[ (dataFrame['id_gimnasio'] == id) & (dataFrame['activo'] == True) ]

    if filtrado.empty:
        return {"Error":"No Existe este gimnasio"}
    else:
        return filtrado.iloc[0].to_dict()

def find_gym_id_company(id: int):
    dataFrame = pd.read_csv('gimnasios.csv')
    company = find_company_id(id)

    if "Error" in company:
        return {"Error":"company no encontrada"}

    company_id = company['id_company']

    gimnasios = dataFrame[dataFrame['id_company'] == company_id]
    return gimnasios.to_dict('records')
