from models.location import Location, LocationId
from models.gymTypes import GymTypes
from sqlmodel import Session, select, and_

async def create_location(location: Location, session: Session):
    new_location = LocationId.model_validate(location)
    session.add(new_location)
    session.commit()
    session.refresh(new_location)
    return new_location

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

def find_one_location(session: Session, id_location: int):
    location = session.exec(select(LocationId).where(LocationId.id_location == id_location)).one_or_none()

    if location is None:
        return None

    return location

