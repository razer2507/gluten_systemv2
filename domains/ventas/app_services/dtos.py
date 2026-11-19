from dataclasses import dataclass
@dataclass
class VentasBusquedaFilter:
    fecha_inicio : str | None = None
    fecha_fin: str | None = None
    id_cliente : int | None = None
    estado : str | None = None
    total_min : float | None = None
    total_max : float | None = None
    