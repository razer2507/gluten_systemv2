import flet as ft

from domains.ventas.presentation.view import VentasView
from shared.ui.sidebar import SideBar


class MainView(ft.Container):
    def __init__(self, ventas_view: VentasView, **kwargs):
        super().__init__(**kwargs)
        self.ventas_view = ventas_view
        self.nav_tab = SideBar(
            vista_venta=self.ventas_view,
            vista_productos=ft.Container(
                content=ft.Text("productos mock up", size=30, color=ft.Colors.WHITE)
            ),
        )
        self.content = self._construir_ui()
        self.expand = True

    def _construir_ui(self):
        return ft.Column(controls=[self.nav_tab])
