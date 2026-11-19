import flet as ft

from domains.ventas.app_services.service import RegistrarVentaUseCase
from domains.ventas.presentation.components.formulario import (
    FormularioVentasComponent,
)
from shared.ui.components import GlutenNormalText


class VentasView(ft.Container):
    def __init__(
        self,
        clientes: list[dict],
        productos: list[dict],
        estados: list[dict],
        page: ft.Page,
        service: RegistrarVentaUseCase,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.formulario = FormularioVentasComponent(
            pagina_principal=page,
            clientes=clientes,
            productos=productos,
            estados=estados,
            on_guardar_venta_click=self.procesar_venta,
        )
        self.content = self.construir_vista()
        self.service = service

    def construir_vista(self):
        return ft.Column(
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            controls=[
                GlutenNormalText(value="Formulario de Ventas", size=32),
                self.formulario,
            ],
        )

    def procesar_venta(self, data):
        return self.service.registrar_venta(**data)
   

