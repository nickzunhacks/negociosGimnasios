from fastapi import FastAPI, Request, UploadFile, HTTPException, Form, File
from sqlmodel import Session

from db.db import get_session
from fastapi.params import Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db.db import Conversation, create_all_tables
from db.operations_db import (create_location,
                              create_company,
                              create_equipment,
                              create_owner,
                              show_companies,
                              show_locations,
                              show_locations_all,
                              show_locations_filtered,
                              show_location_category,
                              show_equipment_gym,
                              show_all_companies,
                              find_one_location,
                              find_owner_email,
                              put_company
                              )
from models import company

from models.gymTypes import GymTypes
from models.location import  Location
from models.company import Company, CompanyUpdate

from middlewares.verificar_img import is_image
from middlewares.suprabase import save_img
from middlewares.geolocation_converter import coordenadas
from middlewares.error import error_handler

from models.equipment import Equipment

from pathlib import Path

from models.owner import Owner

BASE = Path(__file__).resolve().parent

app = FastAPI(lifespan=create_all_tables)
templates = Jinja2Templates(directory=BASE.parent.parent / "frontend" / "templates")
app.mount("/static", StaticFiles(directory=BASE.parent.parent / "frontend" / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def search_gym(request: Request, session: Conversation, mod: str = "person"):
    locations = show_locations_all(session)
    return templates.TemplateResponse(request, "buscador_gym.html", {
        "locations":[loc.model_dump() for loc in locations],
        "acitve_page":"/",
        "mod":mod
        })

@app.get("/locations-company", response_class=HTMLResponse)
async def search_gym(request: Request, session: Conversation, id_company: int, id_owner: int):
    locations = show_locations(session, id_company)

    if len(locations) == 0:
        return error_handler(request, templates, "204", "Esta compañia no tiene gimnasios", "204.jpg", f"/companies?id_owner={id_owner}", f"/locations-company?id_company={id_company}&id_owner={id_owner}")

    return templates.TemplateResponse(request, "buscador_gym.html", {
        "locations":[loc.model_dump() for loc in locations],
        "mod":'owner'
        })

@app.get("/company-edit")
def company_edit(request: Request):
    return templates.TemplateResponse(request, "form_company_edit.html", {})

@app.get("/owner-access")
def get_owner_access(request: Request):
    return templates.TemplateResponse(request, "owner_access.html", {"active_page":"acceso"})

@app.get("/owner")
def owner_access(session: Conversation, request: Request,email: str, password: str):
    owner = find_owner_email(session, email)

    if owner == None:
        return error_handler(request, templates, "404", "dueño no encontrado", "404.jpg", "/","/owner-access")

    elif (owner.password != password):
        return error_handler(request, templates, "401", "clave incorrecta", "401.jpg", "/","/owner-access")

    return RedirectResponse(f"/companies?id_owner={owner.id_owner}")

@app.get("/owner-registration", response_class=HTMLResponse)
async def owner_registration(request: Request):
    return templates.TemplateResponse(request,"form_owner.html", { "active_page":"registro" })

@app.get("/gym-registration", response_class=HTMLResponse)
async def gym_registration(request: Request, id_company: int):
    return templates.TemplateResponse(request,"registro_gym.html", { "active_page":"/gym-registration", "id_company":id_company})

@app.get("/companies-all")
def get_companies_all(session: Conversation, id_owner: int):
    return show_all_companies(session, id_owner)

@app.get("/companies")
def companies(request: Request, session: Conversation, id_owner: int):

    companies = show_all_companies(session, id_owner)

    return templates.TemplateResponse(request, "companies.html", {"owner_id": id_owner, "companies":companies, "acitve_page":"vercompanies"})

@app.get("/company-form")
def get_company_form(request: Request, owner_id: int, mod: str):
    if mod == "registrado":
        registro = "crear"
    else:
        registro = "registro"
    return templates.TemplateResponse(request, "form_company.html", {"owner_id": owner_id, "mod": mod, "active_page":registro })

@app.get("/locations-all")
def get_locations_all(session: Conversation):
    return show_locations_all(session)

@app.get("/locations")
def get_locations(id_company: int, session: Conversation):
    return show_locations(session, id_company)

@app.get("/location-categories")
async def get_location_categories(category: GymTypes, session: Conversation):
    return show_location_category(category, session)

@app.get("/location-search", response_class=HTMLResponse)
async def search_location(name: str, category: GymTypes, session: Conversation, request: Request):
    locations = show_locations_filtered(name, category, session)
    return templates.TemplateResponse(request, "buscador_gym.html", {"locations":[loc.model_dump() for loc in locations], "mod":"person", "active_page":"/"})

@app.get("/location-one")
async def find_location(id_location: int, session: Conversation):
    return find_one_location(session, id_location)

@app.get("/equipment-location")
async def get_equipment_location(id_location: int, session: Conversation):

    equipment = show_equipment_gym(session, id_location)

    if equipment == None:
        raise HTTPException(status_code=404, detail="No equipment or gym inexistent")

    return equipment

@app.post("/location-register")
async def post_location(request: Request,
                        id_company: int = Form(...),
                        name: str = Form(...),
                        description: str = Form(...),
                        address: str = Form(...),
                        type: GymTypes = Form(...),
                        pool: bool = Form(False),
                        pool_number: int = Form(0),
                        boxing_ring: bool = Form(False),
                        boxing_ring_number: int = Form(0),
                        img: UploadFile = File(...),
                        session: Session = Depends(get_session)):

    location_object = Location(id_company = id_company,
                               name = name,
                               description = description,
                               address = address,
                               type_gym = type,
                               pool = pool,
                               pool_number = pool_number,
                               boxing_ring = boxing_ring,
                               boxing_ring_number = boxing_ring_number,)
    image = is_image(img)
    if not(image):
        raise HTTPException(status_code=415, detail="Not an image")

    coord = await coordenadas(location_object.address)

    if (coord == None):
        return error_handler(request, templates, "404", "direccion no encontrada", "404.jpg","/", "/gym-registration")

    print("coordenadas: ", coord)

    location_object.latitude = coord[0]
    location_object.longitude = coord[1]

    try:
        imagen = save_img(img)
    except:
        return error_handler(request, templates, "409", "este nombre de imagen ya existe", "409.jpg", "/", "/gym-registration")

    location_object.photo_url = imagen

    try:
        await create_location(location_object, session)
    except:
        return error_handler(request, templates, "417", "esta compañia no existe", "417.jpg", "/", "/gym-registration")

    if (location_object.pool_number < 0 or location_object.boxing_ring_number < 0):
        return error_handler(request, templates, "417", "numero de pisinas o rings de boxeo deben ser mayor a 0", "400.jpg", "/", "/gym-registration")

    return RedirectResponse("/?mod=owner", status_code=303)

@app.post("/owner-register")
async def post_owner(request: Request,
                     session: Conversation,
                     name: str = Form(...),
                     email: str = Form(...),
                     password: str = Form(...),
                     ):
    owner = Owner(name = name, email = email, password = password)
    new_owner = create_owner(owner, session)

    return RedirectResponse(f"/companies?id_owner={new_owner.id_owner}", status_code=303)

@app.post("/company")
async def post_company(company: Company, session: Conversation):
    return create_company(company, session)

@app.post("/company-register")
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
        return error_handler(request, templates, "409", "este nombre de imagen ya existe", "409.jpg", "/", "")

    company = Company(id_owner=id_owner, name = name, logoUrl=url_img, phone = phone, email = email)
    new_company = await create_company(company, session)

    companies = show_all_companies(session, id_owner)

    return RedirectResponse(f"/companies?id_owner={new_company.id_owner}", status_code=303)

@app.post("/location", response_class=HTMLResponse)
async def post_location(id_company: int = Form(...),
                        name: str = Form(...),
                        description: str = Form(...),
                        address: str = Form(...),
                        type: GymTypes = Form(...),
                        pool: bool = Form(False),
                        pool_number: int = Form(0),
                        boxing_ring: bool = Form(False),
                        boxing_ring_number: int = Form(0),
                        img: UploadFile = File(...),
                        session: Session = Depends(get_session)):

    location_object = Location(id_company = id_company,
                               name = name,
                               description = description,
                               address = address,
                               type_gym = type,
                               pool = pool,
                               pool_number = pool_number,
                               boxing_ring = boxing_ring,
                               boxing_ring_number = boxing_ring_number,)
    image = is_image(img)
    if not(image):
        raise HTTPException(status_code=415, detail="Not an image")

    try:
        imagen = save_img(img)
    except:
        raise HTTPException(status_code=409, detail="Ya existe imagen")

    location_object.photo_url = imagen
    coord = await coordenadas(location_object.address)

    if(coord == None):
        raise HTTPException(status_code=404, detail="Direccion no encontrada")

    print("coordenadas: ", coord)

    location_object.latitude = coord[0]
    location_object.longitude = coord[1]

    return await create_location(location_object, session)

@app.post("/equipment")
async def post_equipment(equipment: Equipment, session: Conversation):
    new_equipment = await create_equipment(equipment, session)

    if new_equipment == None:
        raise HTTPException(status_code=404, detail="gimnasio no encontrado")

    return new_equipment

"""
@app.post("/company-edit")
async def put_company(session: Conversation, id_company: int, request: Request,
                name: str = Form(None),
                email: str = Form(None),
                phone: str = Form(None),):

    update_data = CompanyUpdate(name = name, email = email, phone = phone)
    data = update_data.model_dump(exclude_none=True)

    new_company = await put_company(session, data, id_company)

    if not new_company:
        return error_handler(request, templates, "400", "Al menos enviar un elemento a actualizar",
                             "400.jpg", f"/companies?id_owner={}, "")

    return

"""