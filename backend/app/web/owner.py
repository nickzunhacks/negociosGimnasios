from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from models.owner import Owner
from fastapi.templating import Jinja2Templates
from db.db import Conversation
from db.operations_owner import find_owner_email, create_owner
from middlewares.error import error_handler
from pathlib import Path

BASE = Path(__file__).parent


templates = Jinja2Templates(directory= BASE / "templates")
router = APIRouter()

# ---------------------------------------------------------------| GET |---------------------------------------------------------------

# entrega el form para el acceso a un owner
@router.get("/owner-access")
def get_owner_access(request: Request):
    return templates.TemplateResponse(request, "owner_access.html", {"active_page":"acceso"})

# entrega el form del registro de un nuevo owner
@router.get("/owner-registration", response_class=HTMLResponse)
async def owner_registration(request: Request):
    return templates.TemplateResponse(request,"form_owner.html", { "active_page":"registro" })

# verifica la clave y entrega o error o el home de un owner
@router.get("/owner")
def owner_access(session: Conversation, request: Request,email: str, password: str):
    owner = find_owner_email(session, email)
    if owner == None:
        return error_handler(request, templates, "404", "dueño no encontrado", "404.jpg", "/","/owner-access", "person")
    elif (owner.password != password):
        return error_handler(request, templates, "401", "clave incorrecta", "401.jpg", "/","/owner-access", "person")
    return RedirectResponse(f"/companies?id_owner={owner.id_owner}")

# ---------------------------------------------------------------| POST |---------------------------------------------------------------

# intercepta los datos del form de /owner-registration y registra el gimnasio
@router.post("/owner-register")
async def post_owner(request: Request,
                     session: Conversation,
                     name: str = Form(...),
                     email: str = Form(...),
                     password: str = Form(...),
                     ):
    if(len(password) < 5):
        return templates.TemplateResponse(request,"form_owner.html", { "active_page":"registro", "alert":"true", "alert_msg":"La clave debe de tener 5 caracteres minimo" })
    owner = Owner(name = name, email = email, password = password)
    new_owner = create_owner(owner, session)
    return RedirectResponse(f"/companies?id_owner={new_owner.id_owner}", status_code=303)

# ---------------------------------------------------------------| UPDATE |-------------------------------------------------------------


# ---------------------------------------------------------------| DELETE |-------------------------------------------------------------