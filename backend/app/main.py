from fastapi import FastAPI
from db.db import Conversation, create_all_tables
from db.operations_db import create_location, create_company, show_companies, show_locations, show_locations_all
from models.Location import  Location
from models.Company import Company
from models.Equipment import Equipment

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
def root():
    return {"Hello": "Welcome to gym app"}

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