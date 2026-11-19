import flet as ft

from app.ctx import AppContext
from config.settings import DatabaseSettings
from domains.ventas.presentation.view import VentasView


def main(page: ft.Page) -> None:
    ctx = AppContext(settings=DatabaseSettings.from_env())
    clientes = [cliente.to_dict() for cliente in ctx.cliente_repo.get_all()]
    productos = [producto.to_dict() for producto in ctx.producto_repo.get_all()]
    estados = ["contado", "en deuda"]

    page.add(
        VentasView(
            clientes=clientes,
            productos=productos,
            estados=estados,
            page=page,
            service=ctx.registrar_venta,
        )
    )


if __name__ == "__main__":
    ft.run(main)
