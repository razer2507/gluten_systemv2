from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Producto:
    nombre: str | None = None
    precio_costo: float | None = None
    categoria: str | None = None
    id: int | None = None

    def to_dict(self, exclude_id: bool = False) -> dict:
        data = {
            "nombre": self.nombre,
            "precio_costo": self.precio_costo,
            "categoria": self.categoria,
        }
        if not exclude_id:
            data["id"] = self.id
        return data

    @classmethod
    def from_dict(cls, data: dict | None) -> Producto | None:
        if data is None:
            return None
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            precio_costo=data.get("precio_costo"),
            categoria=data.get("categoria"),
        )
