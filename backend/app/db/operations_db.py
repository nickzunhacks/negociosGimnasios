from sqlmodel import Session, select, or_, and_

from models.gymTypes import GymTypes
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

async def create_location(location: Location, session: Session):
    new_location = LocationId.model_validate(location)
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

def show_location_category(category: GymTypes, session: Session):
    return session.exec(select(LocationId).where(LocationId.type_gym == category)).all()

def show_locations_filtered(name: str, category: GymTypes, session: Session):
    if name == "":
        return show_location_category(category, session)

    return session.exec(
        select(LocationId).where(
            and_(LocationId.name == name, LocationId.type_gym == category)
        )
    ).all()