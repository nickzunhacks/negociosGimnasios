from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path
from db.db import Conversation, create_all_tables
from db.operations_db import create_location, create_company, show_companies, show_locations, show_locations_all
from models.location import  Location
from models.company import Company
from models.equipment import Equipment

#Eliminar proceso de consola trabada

#C:\Users\sala1.FI-LABSISTEMAS.001>tasklist | findstr python
#python.exe                   11552 Console                    2    79.584 KB

#C:\Users\sala1.FI-LABSISTEMAS.001>taskkill /PID 11552 /F
#Correcto: se terminó el proceso con PID 11552.

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(lifespan=create_all_tables)
templates = Jinja2Templates(directory= BASE_DIR.parent.parent / "frontend" / "templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request,"home.html")

@app.get("/companies")
def get_companies(session: Conversation):
    return show_companies(session)

@app.get("/locations-all")
def get_locations_all(session: Conversation):
    return show_locations_all(session)

@app.get("/locations")
def get_locations(id_company: int, session: Conversation):
    return show_locations(session, id_company)

@app.post("/company")
async def post_company(company: Company, session: Conversation):
    return create_company(company, session)

@app.post("/location")
async def post_location(location: Location, session: Conversation):
    return create_location(location, session)