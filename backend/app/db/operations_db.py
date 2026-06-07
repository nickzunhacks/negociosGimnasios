from sqlmodel import Session, select, or_, and_

from models.gymTypes import GymTypes
from models.location import Location, LocationId
from models.company import Company, CompanyId, CompanyUpdate
from models.equipment import EquipmentId, Equipment
from models.owner import Owner, OwnerId
from middlewares.suprabase import delete_img


async def create_company(company: Company, session: Session):
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

async def create_equipment(equipment: Equipment, session: Session):

    print(equipment)

    location = find_one_location(session, equipment.id_location)

    if location is None:
        return None

    new_equipment = EquipmentId.model_validate(equipment)
    session.add(new_equipment)
    session.commit()
    session.refresh(new_equipment)
    return new_equipment

def create_owner(owner: Owner, session: Session):
    new_owner = OwnerId.model_validate(owner)
    session.add(new_owner)
    session.commit()
    session.refresh(new_owner)
    return new_owner

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

def show_equipment_gym(session: Session, id: int):

    location = find_one_location(session, id)

    if location is None:
        return None

    return session.exec( select(EquipmentId).where(EquipmentId.id_location == id) ).all()

def show_all_companies(session: Session, id_owner: int):
    return session.exec((select(CompanyId).where(CompanyId.id_owner == id_owner))).all()

def find_one_company(session: Session, id_company: int):
    company = session.exec(select(CompanyId).where(CompanyId.id_company == id_company)).one_or_none()
    if company is None:
        return None
    return company

def find_one_location(session: Session, id_location: int):
    location = session.exec(select(LocationId).where(LocationId.id_location == id_location)).one_or_none()

    if location is None:
        return None

    return location

def find_owner_email(session: Session, email: str):
    owner = session.exec(select(OwnerId).where(OwnerId.email == email)).one_or_none()

    if owner is None:
        return None

    return owner

async def put_company(session: Session, company: dict, id_company: int):
    if not company:
        return None

    company_db = session.get(CompanyId,id_company)

    company_db.sqlmodel_update(company)
    session.commit()
    session.refresh(company_db)
    return company_db

async def delete_company(session: Session, id_company: int):
     company = find_one_company(session, id_company)
     if company is None:
         return None
     delete_img(company.logoUrl)
     session.delete(company)
     session.commit()
     return company



























