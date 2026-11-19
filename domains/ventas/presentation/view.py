import flet as ft

from domains.ventas.app_services.service import RegistrarVentaUseCase, ListarVentasQuery
from domains.ventas.presentation.components.formulario import (
    FormularioVentasComponent,
)
from domains.ventas.presentation.components.tabla_ventas import TablaVisualizacionVentas
from shared.ui.components import GlutenNormalText
from domains.ventas.app_services.dtos import VentasBusquedaFilter


class VentasView(ft.Container):
    def __init__(
        self,
        clientes,
        productos,
        estados,
        page: ft.Page,
        service: RegistrarVentaUseCase,
        view_service: ListarVentasQuery,
        **kwargs,
    ):
        super().__init__(**kwargs,expand=True)
        self.service = service
        self.listar_service = view_service
        self.formulario = FormularioVentasComponent(
            pagina_principal=page,
            clientes=clientes,
            productos=productos,
            estados=estados,
            on_guardar_venta_click=self.procesar_venta,
        )
        self.filtro_actual = VentasBusquedaFilter()
        self.tabla_ventas = TablaVisualizacionVentas(
            obtener_ventas_callback=self.listar_service.listar_ventas
        )
        self.vista_actual = "formulario"
        self.content = self.construir_vista(vista=self.vista_actual)

    def construir_vista(self, vista: str):
        vista = self._obtener_vista_factory(vista)
        return ft.Column(
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        GlutenNormalText(value="Formulario de Ventas", size=32),
                        ft.TextButton(
                            content="CAMBIAR A VISUALIZACION",
                            on_click=lambda _: self._togglear_vista(),
                        ),
                    ]
                ),
                ft.Container(content=vista),
            ],
        )

    def procesar_venta(self, data):
        return self.service.registrar_venta(**data)

    def _togglear_vista(self):
        if self.vista_actual == "formulario":
            self.vista_actual = "visualizacion"
            self.content = self.construir_vista(vista="visualizacion")
        else:
            self.vista_actual = "visualizacion"
            self.content = self.construir_vista(vista="formulario")

        self.update()

    def _obtener_vista_factory(self, vista: str) -> ft.Container:
        vistas_map = {"formulario": self.formulario, "visualizacion": self.tabla_ventas}
        return vistas_map.get(vista)
