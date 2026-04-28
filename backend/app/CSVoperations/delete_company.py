import pandas as pd
from CSVoperations.find_company import find_company_id
from CSVoperations.find_gym import find_gym_id_company
from CSVoperations.delete_gym import delete_gym

def delete_company(id:int):
    company = find_company_id(id)

    if "Error" in company:
        return company

    delete_related_gym(id)

    dataFrame = pd.read_csv('companies.csv')
    dataFrame.loc[dataFrame['id_company'] == id, 'activo'] = False
    dataFrame.to_csv('companies.csv', index=False)

    return {"Exito": "Se elimino correctamente company"}

def delete_related_gym(id:int):
    list_gyms = find_gym_id_company(id)

    for gym in list_gyms:
        delete_gym(gym['id_gimnasio'])