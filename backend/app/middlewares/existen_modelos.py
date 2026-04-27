from pathlib import Path

ruta = Path.cwd()

def necesitanCrearse() -> bool:

    lista_archivos_necesarios = ["gimnasios.csv","equipment.csv","companies.csv"]

    estanTodos = True

    for i in lista_archivos_necesarios:
        if not Path(ruta/i).exists():
            estanTodos = False
            print("no existe ",i)

    return not estanTodos

