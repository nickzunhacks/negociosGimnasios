from sqlmodel import Session, select, and_
from models.company import Company, CompanyId, CompanyUpdate
from middlewares.suprabase import delete_img

async def create_company(company: Company, session: Session):
    new_company = CompanyId.model_validate(company)
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    return new_company

def show_companies(session: Session):
    companies = session.exec(select(CompanyId)).all()
    return companies

def show_all_companies(session: Session, id_owner: int):
    return session.exec((select(CompanyId).where(CompanyId.id_owner == id_owner))).all()

def find_one_company(session: Session, id_company: int):
    company = session.exec(select(CompanyId).where(CompanyId.id_company == id_company)).one_or_none()
    if company is None:
        return None
    return company

async def put_company(session: Session, company: dict, id_company: int):
    if not company:
        return None

    company_db = session.get(CompanyId, id_company)

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