from fastapi import APIRouter
from db.db import Conversation
from db.operations_company import create_company, show_all_companies
from models.company import Company

router = APIRouter()

# --------------------------------| GET |--------------------------------

#entrega todas las empresas existentes
@router.get("/companies-all")
def get_companies_all(session: Conversation, id_owner: int):
    return show_all_companies(session, id_owner)

# --------------------------------| POST |--------------------------------

# registra una compania
@router.post("/company")
async def post_company(company: Company, session: Conversation):
    return create_company(company, session)