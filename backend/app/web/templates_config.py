from fastapi.templating import Jinja2Templates
from pathlib import Path
BASE = Path(__file__).resolve().parent

templates = Jinja2Templates(BASE / "templates")