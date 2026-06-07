from fastapi import Request

def error_handler(request: Request, templates, error_code: str, error_msg: str, img_name: str, volver_url: str, reintentar_url: str, mod: str):
    return templates.TemplateResponse(request, "error.html", {
        "error_code": error_code,
        "error_msg": error_msg,
        "imagen": img_name,
        "volver": volver_url,
        "reintentar": reintentar_url,
        "mod": mod
    })