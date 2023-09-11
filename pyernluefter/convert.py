from datetime import datetime
from enum import Enum


class SystemMode(Enum):
    Zeitgesteuert = "Zeitgesteuert"
    Kellermode = "Kellermode"
    Behaglichkeitsmode = "Behaglichkeitsmode"


def comma_float(x:str):
    if x == "N/A":
        return None
    return float(x.replace(",", "."))


CONVERSION_DICT = {
    "Date": lambda x: datetime.strptime(x, "%d.%m.%Y").date(),
    "Time": lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    "MAC": lambda x: hex(int(x, 16)),
    "RSSI": int,
    "SystemMode": lambda x: SystemMode(x),
    "Speed_In": int,
    "Speed_Out": int,
    "Speed_AntiFreeze": int,
    "Temp_In": comma_float,
    "Temp_Out": comma_float,
    "Temp_Fresh": comma_float,
    "rel_Humidity_In": comma_float,
    "rel_Humidity_Out": comma_float,
    "abs_Humidity_In": comma_float,
    "abs_Humidity_Out": comma_float,
    "Efficiency": comma_float,
    "Humidity_Transport": int,
    "_SystemOn": lambda x: x == "1",
    "_FrostschutzAktiv": bool,
    "_Frozen": bool,
    "_AbtauMode": bool,
    "_VermieterMode": bool,
    "_QuerlueftungAktiv": bool,
    "_MaxMode": bool,
}
