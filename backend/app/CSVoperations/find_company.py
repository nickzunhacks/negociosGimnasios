import pandas as pd

def find_company_id(id:int):
    dataFrame = pd.read_csv('companies.csv')
    filtrado = dataFrame[dataFrame['id_company'] == id]

    if filtrado.empty:
        print("company no encontrado")
        return {"Error":"Este company no existe"}
    else:
        print("company encontrado")
        return filtrado.iloc[0].to_dict()