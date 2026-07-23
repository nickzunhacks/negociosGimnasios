from fastapi import APIRouter, Request, UploadFile, Form,File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.company import Company, CompanyUpdate
from db.db import Conversation
from pathlib import Path
from middlewares.error import error_handler
from db.operations_location import show_locations
from db.operations_company import show_all_companies, create_company, find_one_company, put_company, delete_company
from middlewares.suprabase import save_img, delete_img

router = APIRouter()
BASE = Path(__file__).resolve().parent

templates = Jinja2Templates(directory= BASE / "templates" )

# ---------------------------------------------------------------| GET |---------------------------------------------------------------

# Entrega todas los gimnasios de una empresa
@router.get("/locations-company", response_class=HTMLResponse)
async def search_gym(request: Request, session: Conversation, id_company: int, id_owner: int):
    locations = show_locations(session, id_company)
    if len(locations) == 0:
        return error_handler(request, templates, "204", "Esta compañia no tiene gimnasios", "204.jpg", f"/companies?id_owner={id_owner}", f"/locations-company?id_company={id_company}&id_owner={id_owner}", "owner")
    return templates.TemplateResponse(request, "buscador_gym.html", {
        "locations":[loc.model_dump() for loc in locations],
        "mod":'owner',
        "owner_id":id_owner,
        })

#entrega todas las empresas pero en html
@router.get("/companies")
def companies(request: Request, session: Conversation, id_owner: int):
    companies = show_all_companies(session, id_owner)
    if len(companies) == 0:
        return templates.TemplateResponse(request, "companies.html", {"owner_id": id_owner, "companies":companies, "acitve_page":"vercompanies", "alert":"true", "alert_msg":" Crea tu compañía para agregar tus gimnasios"})
    return templates.TemplateResponse(request, "companies.html", {"owner_id": id_owner, "companies":companies, "acitve_page":"vercompanies"})

# entrega el form del registro de una empresa
@router.get("/company-form")
def get_company_form(request: Request, owner_id: int):
    return templates.TemplateResponse(request, "form_company.html", {"owner_id": owner_id, "mod": "owner", "active_page":"registro" })

# Entrega el form para actualizar a una empresa
@router.get("/company-edit")
def company_edit(request: Request, id_company: int, id_owner: int):
    return templates.TemplateResponse(request, "form_company_update.html", {"id_company":id_company, "id_owner":id_owner})

# ---------------------------------------------------------------| POST |---------------------------------------------------------------

# obtiene los datos del form de /company-form y registra la emrpesa
@router.post("/company-register")
async def post_company(request: Request, session: Conversation,
                       id_owner: int = Form(...),
                       name: str = Form(...),
                       email: str = Form(...),
                       phone: str = Form(...),
                       image: UploadFile = File(...),):
    print(id_owner)
    try:
        url_img = save_img(image)
    except:
        return error_handler(request,
                             templates,
                             "409",
                             "este nombre de imagen ya existe",
                             "409.jpg",
                             f"/companies?id_owner={id_owner}",
                             f"/company-form?owner_id={id_owner}",
                             "owner"
                             )
    company = Company(id_owner=id_owner, name = name, logoUrl=url_img, phone = phone, email = email)
    new_company = await create_company(company, session)
    companies = show_all_companies(session, id_owner)
    return RedirectResponse(f"/companies?id_owner={new_company.id_owner}", status_code=303)

# ---------------------------------------------------------------| UPDATE |---------------------------------------------------------------

# edita una empresa, los campos recibidos son opcionales
@router.post("/company-edit")
async def edit_company(session: Conversation, request: Request,
                id_company: int = Form(...),
                id_owner: int = Form(...),
                name: str | None = Form(default=None),
                email: str | None = Form(default=None),
                phone: str | None = Form(default=None),
                image: UploadFile | None = Form(default=None),):
    print(name)
    print(email)
    print(phone)
    print(image)
    update_data = CompanyUpdate(name = name, email = email, phone = phone)
    if image.filename != "":
        company = find_one_company(session, id_company)
        delete_img(company.logoUrl)
        new_url = save_img(image)
        update_data.logoUrl = new_url
    data = update_data.model_dump(exclude_none=True)
    new_company = await put_company(session, data, id_company)
    if not new_company:
        return error_handler(request, templates,
                             "400",
                             "Al menos enviar un elemento a actualizar",
                             "400.jpg",
                             f"/companies?id_owner={id_owner}",
                             f"/company-edit?id_company={id_company}&id_owner={id_owner}",
                             "owner")
    return RedirectResponse(f"/companies?id_owner={id_owner}", status_code=303)

# ---------------------------------------------------------------| DELETE |---------------------------------------------------------------

# borra una empresa
@router.post("/company-delete")
async def company_delete(session: Conversation,
                   id_company: int = Form(...),
                   id_owner: int = Form(...),):
    await delete_company(session, id_company)
    return RedirectResponse(f"/companies?id_owner={id_owner}", status_code=303)