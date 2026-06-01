from sqlmodel import Session, select
from models.location import Location, LocationId
from models.company import Company, CompanyId

def create_company(company: Company, session: Session):
    new_company = CompanyId.model_validate(company)
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    return new_company

def create_location(location: Location, session: Session):
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