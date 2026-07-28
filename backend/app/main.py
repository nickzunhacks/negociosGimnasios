from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.db import Conversation, create_all_tables
from db.operations_location import show_locations_all
from pathlib import Path
from web import company as web_company, equipment as web_equipment,location as web_location, owner as web_owner
from web.templates_config import templates

BASE = Path(__file__).resolve().parent
app = FastAPI(lifespan=create_all_tables)
# base es la ubucacion
app.mount("/static", StaticFiles(directory=BASE.parent.parent / "frontend" / "static"), name="static")

#ROOT
#el root es el buscador de gimnasios
@app.get("/", response_class=HTMLResponse)
async def search_gym(request: Request, session: Conversation, mod: str = "person"):
    locations = show_locations_all(session)
    return templates.TemplateResponse(request, "location/buscador_gym.html", {
        "locations":[loc.model_dump() for loc in locations],
        "active_page":"/",
        "mod":mod
        })

#importamos los endpoints
app.include_router(web_company.router)
app.include_router(web_owner.router)
app.include_router(web_location.router)