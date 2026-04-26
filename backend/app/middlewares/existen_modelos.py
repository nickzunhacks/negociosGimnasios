from pathlib import Path

ruta = Path(__file__).parent.parent.parent.parent

def necesitanCrearse() -> bool:

    lista_archivos_necesarios = ["gimnasios.csv","equipment.csv"]

    estanTodos = True

    for i in lista_archivos_necesarios:
        if not Path(ruta/i).exists():
            estanTodos = False
            print("no existe ",i)

    return estanTodos

