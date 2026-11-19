from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Cliente:
    nombre: str
    referencia: str
    id: int | None = None

    def to_dict(self, exclude_id: bool = False) -> dict:
        data = {
            "nombre": self.nombre,
            "referencia": self.referencia,
        }
        if not exclude_id:
            data["id"] = self.id
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Cliente:
        if data is None:
            return None
        return cls(
            id=data.get("id"),
            nombre=data.get("nombre"),
            referencia=data.get("referencia"),
        )
