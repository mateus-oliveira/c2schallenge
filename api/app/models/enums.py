from enum import Enum


class Transmission(Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATICO"
    CVT = "CVT"


class Fuel(Enum):
    GASOLINE = "GASOLINA"
    DIESEL = "DIESEL"
    FLEX = "FLEX"
    ELECTRIC = "ELETRICO"
    HYBRID = "HIBRIDO"
