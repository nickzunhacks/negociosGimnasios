from models.equipment import EquipmentId, Equipment
from models.gimnasio import GimnasioEntrada, GimnasioEntrada, GimnasioSalida


def put_id_gym_equipment(gimnasio: GimnasioEntrada):

    equipment:list[EquipmentId] = []

    for i in gimnasio.equipment:
        print(i)
        equipment.append(EquipmentId(id_gym=gimnasio.id_gimnasio,category=i.category, description=i.description,id_equipment=i.id_equipment,name=i.name))

    nuevo_gimnasio = GimnasioSalida(equipment=equipment,**gimnasio.model_dump(exclude={'equipment'}))

    return nuevo_gimnasio
