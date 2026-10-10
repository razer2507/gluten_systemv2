from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import datetime


@dataclass
class Venta:
    fecha: datetime
    cliente_id: int
    total: float
    estado: str
    productos: list[DetalleVenta]
    id: int | None = None

    def __str__(self):
        productos_str = "".join([str(detalle) for detalle in self.productos])
        return f"{'=' * 20}\nFECHA:{self.fecha}\nID:{self.id}\nCLIENTE ID:{self.cliente_id}\nTOTAL:{self.total}\nESTADO:{self.estado}\nPRODUCTOS:\n{'-'*20}{productos_str}\n{'=' * 20}"

    def __len__(self):
        return len(fields(self))

    # OBJ -> SQL
    def to_dict(self, exclude_id: bool = False) -> dict:
        data = {
            "fecha": self.fecha,
            "cliente_id": self.cliente_id,
            "total": self.total,
            "estado": self.estado,
        }
        if not exclude_id:
            data["id"] = self.id
        return data

    # SQL -> OBJ
    @classmethod
    def from_dict(cls, data: dict) -> Venta:
        return (
            cls(
                id=data.get("id"),
                fecha=data.get("fecha"),
                cliente_id=data.get("cliente_id"),
                total=data.get("total"),
                estado=data.get("estado"),
                productos=[
                    DetalleVenta.from_dict(producto)
                    for producto in data.get("productos")
                ],
            )
            if data != None
            else None
        )


@dataclass
class DetalleVenta:
    producto_id: int
    cantidad: int
    precio_unitario: float
    id: int | None = None
    venta_id: int | None = None

    def __str__(self):
        return f"\nID:PRODUCTO {self.producto_id}\nCANTIDAD VENDIDA:{self.cantidad}\nPRECIO UNIT:{self.precio_unitario}\nVENTA_ID:{self.venta_id}\n"

    @classmethod
    def __len__(self):
        return len(fields(self))

    #OBJ -> SQL
    def to_dict(self, venta_padre_id: int | None = None) -> dict:
        data = {
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
        }
        if venta_padre_id is not None:
            data["venta_id"] = venta_padre_id
        return data

    #SQL -> OBJ
    @classmethod
    def from_dict(cls, data: dict) -> DetalleVenta:
        return (
            cls(
                id=data.get("id"),
                venta_id=data.get("venta_id"),
                producto_id=data.get("producto_id"),
                cantidad=data.get("cantidad"),
                precio_unitario=data.get("precio_unitario"),
            )
            if data != None
            else None
        )
