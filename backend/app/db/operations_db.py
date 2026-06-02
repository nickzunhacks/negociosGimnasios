from sqlmodel import Session, select
from fastapi import UploadFile
from models.location import Location, LocationId
from models.company import Company, CompanyId
from middlewares.geolocation_converter import coordenadas
from middlewares.suprabase import save_img

def create_company(company: Company, session: Session):
    new_company = CompanyId.model_validate(company)
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    return new_company

async def create_location(location: Location, img: UploadFile, session: Session):
    new_location = LocationId.model_validate(location)
    print(f"Buscando: {new_location.address}...")
    coord = await coordenadas(location.address)
    print(f"resultado: {coord}")
    print("guardando imagen...")
    imagen = save_img(img)
    print("imagen guardada!: ", imagen)
    new_location.latitude = coord[0]
    new_location.longitude = coord[1]
    new_location.photo_url = imagen
    session.add(new_location)
    session.commit()
    session.refresh(new_location)
    return new_location

def show_companies(session: Session):
    companies = session.exec(select(CompanyId)).all()
    return companies

def show_locations_all(session: Session):
    locations = session.exec(select(LocationId)).all()
    return locations

def show_locations(session: Session, id_company: int):
    locations = session.exec(select(LocationId).where(LocationId.id_company == id_company)).all()
    return locations