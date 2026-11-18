from datetime import datetime
def to_dropdown_option(keys: list, values: list) -> list:
    if not isinstance(keys, list):
        raise TypeError
    if not isinstance(values, list):
        raise TypeError

    return list(zip(keys, values))

def from_flet_str_to_datetime(str)->datetime:
    # Tu fecha original con barras
    fecha_original = "06/14/2026"

    # 1. Leer el formato original (Mes/Día/Año)
    objeto_fecha = datetime.strptime(fecha_original, "%m/%d/%Y")

    # 2. Exportar al formato ISO (Año-Mes-Día)
    fecha_final = objeto_fecha.strftime("%Y-%m-%d")

    return fecha_final