from fastapi import APIRouter, Depends, HTTPException, File, Form, Request,UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from models.location import Location,GymTypes
from sqlmodel import Session
from db.db import get_session, Conversation
from middlewares.verificar_img import is_image
from middlewares.geolocation_converter import coordenadas
from middlewares.error import error_handler
from middlewares.suprabase import save_img
from db.operations_location import show_locations_filtered, create_location
from db.operations_company import find_one_company
from web.templates_config import templates

router = APIRouter()


# ---------------------------------------------------------------| GET |---------------------------------------------------------------

#entrega el form del registro de un nuevo gym
@router.get("/gym-registration", response_class=HTMLResponse)
async def gym_registration(request: Request, id_company: int):
    return templates.TemplateResponse(request,"location/registro_gym.html", { "active_page":"/gym-registration", "id_company":id_company})

# busca los gimnaios por categoria y nombre, si nombre no es enviado solo filtra por categorias
@router.get("/location-search", response_class=HTMLResponse)
async def search_location(name: str, category: GymTypes, session: Conversation, request: Request):
    locations = show_locations_filtered(name, category, session)
    return templates.TemplateResponse(request, "location/buscador_gym.html", {"locations":[loc.model_dump() for loc in locations], "mod":"person", "active_page":"/"})

# ---------------------------------------------------------------| POST |---------------------------------------------------------------

# intercepta los datos del form en /gym-registration
@router.post("/location-register")
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
    company = find_one_company(session, id_company)
    coord = await coordenadas(location_object.address)
    if (coord == None):
        return error_handler(request, templates, "404", "direccion no encontrada", "404.jpg",f"/companies?id_owner={company.id_owner}", f"/gym-registration?id_company={company.id_company}", "owner")
    print("coordenadas: ", coord)
    location_object.latitude = coord[0]
    location_object.longitude = coord[1]
    try:
        imagen = save_img(img)
    except:
        return error_handler(request, templates, "409", "este nombre de imagen ya existe", "409.jpg", f"/companies?id_owner={company.id_owner}", f"/gym-registration?id_company={company.id_company}","owner")
    location_object.photo_url = imagen
    try:
        await create_location(location_object, session)
    except:
        return error_handler(request, templates, "417", "esta compañia no existe", "417.jpg", "/", "/gym-registration","owner")
    if (location_object.pool_number < 0 or location_object.boxing_ring_number < 0):
        return error_handler(request, templates, "417", "numero de pisinas o rings de boxeo deben ser mayor a 0", "400.jpg", f"/companies?id_owner={company.id_owner}", f"/gym-registration?id_company={company.id_company}", "owner")
    return RedirectResponse(f"locations-company?id_company={id_company}&id_owner={company.id_owner}", status_code=303)

# ---------------------------------------------------------------| UPDATE |-------------------------------------------------------------


# ---------------------------------------------------------------| DELETE |-------------------------------------------------------------
