import string
from enum import Enum

class EquipmentTypes(str, Enum):

    CARDIOVASCULAR_MACHINE = "cardiovascular machine"
    STRENGTH_MACHINE = "strength machine"
    DUMBBELLS = "dumbbells"
    BENCH = "bench"
    ELASTIC_BAND ="elastic band"
    OTHER = "other"


