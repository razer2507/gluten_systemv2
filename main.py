import flet as ft

from app.ctx import AppContext
from config.settings import DatabaseSettings
from domains.ventas.presentation.view import VentasView
from shared.ui.main_view import MainView


def main(page: ft.Page) -> None:
    page.bgcolor = ft.Colors.BLACK
    settings = DatabaseSettings.from_env()
    app_context = AppContext(settings)
    clientes = [cliente.to_dict() for cliente in app_context.clientes_repo.get_all()]
    productos = [
        producto.to_dict() for producto in app_context.productos_repo.get_all()
    ]

    main_view = MainView(
        ventas_view=VentasView(
            page=page,
            clientes=clientes,
            productos=productos,
            estados=["contado", "credito"],
            service=app_context.registrar_venta_case,
            view_service=app_context.lista_ventas_query,
        )
    )

    page.add(main_view)


if __name__ == "__main__":
    ft.run(main)
