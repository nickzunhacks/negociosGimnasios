import csv
from models.company import CompanySalida, CompanyEntrada
import pandas as pd

def new_id_company():
    dataFrame = pd.read_csv('companies.csv')
    max_id = dataFrame['id_company'].max()

    if pd.isna(max_id):
        return 1

    return max_id+1

def new_company_salida(company: CompanyEntrada):
    id = new_id_company()
    companySalida = CompanySalida(**company.model_dump(),id_company=id)
    columnas = companySalida.model_dump().keys()

    with open('companies.csv','a',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columnas)
        writer.writerow(companySalida.model_dump())

    return companySalida
