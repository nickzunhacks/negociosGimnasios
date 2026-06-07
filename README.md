# gymapp 🏋️

Aplicación web fullstack para la gestión de negocios de gimnasios. Permite a los dueños registrar sus empresas, sedes y equipamiento desde una interfaz web sencilla.

**Deployment:** [https://negociosgimnasios.onrender.com](https://negociosgimnasios.onrender.com)

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI |
| ORM | SQLModel |
| Base de datos | NeonDB (PostgreSQL) |
| Frontend | Jinja2 + Bootstrap 5 |
| Almacenamiento de imágenes | Supabase Storage |
| Deployment | Render |

---

## Modelos de datos

### Owner
Dueño o administrador de uno o más negocios de gimnasios.

### Company
Empresa o marca de gimnasio asociada a un owner. Contiene información como nombre, teléfono, email y logo (almacenado en Supabase).

### Location
Sede o gimnasio físico perteneciente a una company. Contiene información de ubicación geolocalizada.

### Equipment
Equipamiento disponible en una sede.

### Relaciones

```
Owner
  └── Company (1:N)
        └── Location (1:N)
              └── Equipment (1:N)
```

---

## Funcionalidades principales

- Registro y autenticación de owners
- CRUD de companies (con subida y eliminación de logos en Supabase)
- CRUD de locations con mapa interactivo (Leaflet.js + Nominatim)
- CRUD de equipment por sede
- Modal de confirmación para acciones destructivas (delete)
- Alertas de feedback tras operaciones

---

## Estructura del proyecto

```
gymapp/
├── main.py                  # Entrypoint FastAPI, definición de endpoints
├── models.py                # Modelos SQLModel (Owner, Company, Location, Equipment)
├── database.py              # Conexión a NeonDB
├── static/
│   ├── css/
│   │   ├── personalized.css
│   │   └── home.css
│   └── deleteModal.js       # Lógica JS para modal de confirmación de delete
└── templates/
    ├── base.html            # Template base con Bootstrap
    ├── navbarowner.html     # Navbar del owner
    ├── alert.html           # Componente de alertas
    ├── warning.html         # Modal de confirmación (delete)
    ├── companies.html       # Vista de companies del owner
    ├── card_company.html    # Card individual de company
    └── ...
```

---

## Configuración

### Variables de entorno

Crea un archivo `.env` en la raíz con las siguientes variables:

```env
DATABASE_URL=postgresql://...         # Connection string de NeonDB
SUPABASE_URL=https://....supabase.co
SUPABASE_KEY=your_supabase_key
SUPABASE_BUCKET=gym_app
```

### Instalación local

```bash
# Clonar el repositorio
git clone <repo-url>
cd gymapp

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Correr el servidor
uvicorn main:app --reload
```

La app estará disponible en `http://127.0.0.1:8000`.

---

## Notas de base de datos

La base de datos usa **NeonDB (PostgreSQL)**. Las foreign keys entre tablas tienen `ON DELETE CASCADE` para garantizar que al eliminar una company se eliminen automáticamente sus locations asociadas.

Las imágenes de logos se almacenan en **Supabase Storage** bajo el bucket `gym_app`. Las políticas RLS de Supabase están configuradas para permitir subida y eliminación desde el backend.

---

## Deployment

La app está desplegada en **Render** con las variables de entorno configuradas en el dashboard. El deployment se actualiza automáticamente al hacer push a la rama principal.

URL pública: [https://negociosgimnasios.onrender.com](https://negociosgimnasios.onrender.com)
