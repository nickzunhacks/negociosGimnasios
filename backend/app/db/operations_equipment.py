from sqlmodel import Session, select
from models.equipment import EquipmentId, Equipment
from db.operations_location import find_one_location

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

def show_equipment_gym(session: Session, id: int):

    location = find_one_location(session, id)

    if location is None:
        return None

    return session.exec( select(EquipmentId).where(EquipmentId.id_location == id) ).all()
