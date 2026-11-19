from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Gasto:
    categoria: str
    monto: float
    fecha: datetime | str | None = None
    descripcion: str | None = None
    tipo: str | None = None
    id: int | None = None

    def to_dict(self, exclude_id: bool = False) -> dict:
        data = {
            "fecha": self.fecha,
            "categoria": self.categoria,
            "monto": self.monto,
            "descripcion": self.descripcion,
            "tipo": self.tipo,
        }
        if not exclude_id:
            data["id"] = self.id
        return data

    @classmethod
    def from_dict(cls, data: dict | None) -> Gasto | None:
        if data is None:
            return None
        return cls(
            id=data.get("id"),
            fecha=data.get("fecha"),
            categoria=data.get("categoria"),
            monto=data.get("monto"),
            descripcion=data.get("descripcion"),
            tipo=data.get("tipo"),
        )
