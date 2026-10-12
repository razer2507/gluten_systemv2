from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import date

from shared.exceptions import (
    EstadoInvalidoError,
    FechaInvalidaError,
    TotalInvalidoError,
    VentaSinProductosError,
)


@dataclass
class Venta:
    fecha: date | str
    cliente_id: int
    total: float
    estado: str
    productos: list[DetalleVenta]
    id: int | None = None

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
    
    @property
    def subtotal(self):
        return sum(producto.subtotal_item for producto in self.productos)

  
    def __post_init__(self) -> None:
        self._validar_estado()
        self._validar_fecha()
        self._validar_productos()
        self._validar_total()
        


    def _validar_estado(self) -> None:
        if not isinstance(self.estado,str):
            raise EstadoInvalidoError("El estado de la venta no es un texto")

    def _validar_fecha(self) -> None:
        if not isinstance(self.fecha,str | date):
            raise FechaInvalidaError('La fecha no es un dato valido')
        if isinstance(self.fecha, str):
            try:
                date.fromisoformat(self.fecha)
            except ValueError:
                raise FechaInvalidaError('Formato invalido para la fecha (YY-MM-DD)')
    
    def _validar_productos(self) -> None:
        if len(self.productos) == 0:
            raise VentaSinProductosError("No hay productos para la venta.")
        if not isinstance(self.productos,list):
            raise VentaSinProductosError(
                "Los productos no satisfacen la estructura de datos requerida."
            )

    def _validar_total(self) -> None:
        try:
            float(self.total)
        except ValueError:
            raise TotalInvalidoError("El dato ingresado no es un total valido (debe ser un numero decimal)")
        if not self.total >= 1:
            raise TotalInvalidoError("El total debe ser mayor o igual a 1")

    def __str__(self) -> str:
        productos_str = "".join([str(detalle) for detalle in self.productos])
        return f"{'=' * 20}\nFECHA:{self.fecha}\nID:{self.id}\nCLIENTE ID:{self.cliente_id}\nSUBTOTAL:{self.subtotal}\nTOTAL:{self.total}\nESTADO:{self.estado}\nPRODUCTOS:\n{'-'*20}{productos_str}\n{'=' * 20}"

    def __len__(self)->int:
        return len(fields(self))
    
@dataclass
class DetalleVenta:
    producto_id: int
    cantidad: int
    precio_unitario: float
    id: int | None = None
    venta_id: int | None = None

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
    
    @property
    def subtotal_item(self):
        return self.cantidad * self.precio_unitario

    def __post_init__(self):
        self._validar_cantidad()
        self._validar_precio_unitario()

    def __str__(self):
        return f"\nID:PRODUCTO {self.producto_id}\nCANTIDAD VENDIDA:{self.cantidad}\nPRECIO UNIT:{self.precio_unitario}\nVENTA_ID:{self.venta_id}\n"

    @classmethod
    def __len__(self):
        return len(fields(self))

    def _validar_precio_unitario(self):
        try:
            float(self.precio_unitario)
        except ValueError:
            raise VentaSinProductosError("El precio unitario no es un decimal valido.")


        if not self.precio_unitario >= 1:
            raise VentaSinProductosError("El precio unitario debe ser un numero positivo")

    def _validar_cantidad(self):
        if not isinstance(self.cantidad,int):
            raise VentaSinProductosError()
        if not self.cantidad >= 1:
            raise VentaSinProductosError() 