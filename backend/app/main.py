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
                              show_companies,
                              show_locations,
                              show_locations_all,
                              show_locations_filtered,
                              show_location_category,
                              show_equipment_gym,
                              find_one_location,
                              )

from models.gymTypes import GymTypes
from models.location import  Location
from models.company import Company
from middlewares.verificar_img import is_image
from middlewares.suprabase import save_img
from middlewares.geolocation_converter import coordenadas
from models.equipment import Equipment
from pathlib import Path

BASE = Path(__file__).resolve().parent

app = FastAPI(lifespan=create_all_tables)
templates = Jinja2Templates(directory=BASE.parent.parent / "frontend" / "templates")
app.mount("/static", StaticFiles(directory=BASE.parent.parent / "frontend" / "static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def search_gym(request: Request, session: Conversation):
    locations = show_locations_all(session)
    return templates.TemplateResponse(request, "buscador_gym.html", {
        "locations":[loc.model_dump() for loc in locations],
        "acitve_page":"/"
        }
    )

@app.get("/gym-registration", response_class=HTMLResponse)
async def gym_registration(request: Request):
    return templates.TemplateResponse(request, "registro_gym.html", { "active_page":"/gym-registration" })

@app.get("/companies")
def get_companies(session: Conversation):
    return show_companies(session)

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
    print("locations al presionar boton:\n\n", locations)
    return templates.TemplateResponse(request, "buscador_gym.html", {"locations":[loc.model_dump() for loc in locations]})

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
                        id_company: int = Form(1),
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
        return templates.TemplateResponse(request, "error.html", {
            "error_code":"404",
            "error_msg":"direccion no encontrada",
            "imagen":"404.jpg"
        })

    print("coordenadas: ", coord)

    location_object.latitude = coord[0]
    location_object.longitude = coord[1]

    try:
        imagen = save_img(img)
    except:
        return templates.TemplateResponse(request, "error.html", {
            "error_code": "409",
            "error_msg": "este nombre de imagen ya existe",
            "imagen": "409.jpg"
        })

    location_object.photo_url = imagen

    try:
        await create_location(location_object, session)
    except:
        return templates.TemplateResponse(request, "error.html", {
            "error_code": "417",
            "error_msg": "esta compania no existe",
            "imagen": "417.jpg"
        })

    return RedirectResponse("/", status_code=303)

@app.post("/company")
async def post_company(company: Company, session: Conversation):
    return create_company(company, session)

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
