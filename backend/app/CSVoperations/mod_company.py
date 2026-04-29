import pandas as pd
from pandas import read_csv

from CSVoperations.find_company import find_company_id

def edit_name(name: str, id: int):

    company = find_company_id(id)

    if "Error" in company:
        return {"Error":"Esta company no existe"}

    dataFrame = pd.read_csv("companies.csv")
    dataFrame.loc[dataFrame['id_company'] == id, 'name'] = name
    dataFrame.to_csv("companies.csv", index=False)

    updated_company = dataFrame[dataFrame['id_company'] == id].iloc[0]

    return updated_company.to_dict()