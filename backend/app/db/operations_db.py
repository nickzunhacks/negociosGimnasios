from sqlmodel import Session, select
from models.Location import Location
from models.Company import Company

def create_company(company: Company, session: Session):
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

def create_location(location: Location, session: Session):
    session.add(location)
    session.commit()
    session.refresh(location)
    return location

def show_companies(session: Session):
    companies = session.exec(select(Company)).all()
    return companies

def show_locations_all(session: Session):
    locations = session.exec(select(Location)).all()
    return locations

def show_locations(session: Session, id_company: int):
    locations = session.exec(select(Location).where(Location.id_company == id_company)).all()
    return locations