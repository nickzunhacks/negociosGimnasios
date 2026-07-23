from models.owner import Owner, OwnerId
from sqlmodel import Session, select, and_

def create_owner(owner: Owner, session: Session):
    new_owner = OwnerId.model_validate(owner)
    session.add(new_owner)
    session.commit()
    session.refresh(new_owner)
    return new_owner

def find_owner_email(session: Session, email: str):
    owner = session.exec(select(OwnerId).where(OwnerId.email == email)).one_or_none()

    if owner is None:
        return None

    return owner