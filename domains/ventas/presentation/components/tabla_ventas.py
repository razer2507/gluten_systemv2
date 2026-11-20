import flet as ft

from domains.ventas.app_services.dtos import VentasBusquedaFilter
from shared.ui.components import GlutenNormalText, VentasFilterDialog


class TablaVisualizacionVentas(ft.Container):
    def __init__(self, obtener_ventas_callback: callable(), **kwargs):
        super().__init__(**kwargs)
        self.bgcolor = ft.Colors.BLACK
        self.obtener_ventas_callback = obtener_ventas_callback
        self.filtro = VentasBusquedaFilter()
        self.filtro_dialog = VentasFilterDialog(on_actualizar=self._actualizar_tabla)
        self.content = self._construir_tabla()

    def _obtener_filas(self):
        ventas = self.obtener_ventas_callback(self.filtro) or []
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(venta.id), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(str(venta.fecha), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(str(venta.cliente_id), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(str(venta.total), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(str(venta.estado), color=ft.Colors.WHITE)),
                ]
            )
            for venta in ventas
        ]

    def _actualizar_tabla(self, params: dict):
        valores = {k: v for k, v in params.items() if v not in (None, "")}
        self.filtro = VentasBusquedaFilter(**valores)
        self.content = self._construir_tabla()
        self.page.pop_dialog()
        self.update()

    def _construir_tabla(self):
        return ft.Column(
            expand=True,  # Necesario para que el scroll tenga un límite de altura
            controls=[
                ft.TextButton(
                    content="Configurar Filtro",  # Nota: usa 'text' en lugar de 'content' para strings
                    on_click=lambda _: self.page.show_dialog(self.filtro_dialog),
                ),
                ft.Column(
                    expand=True,
                    height=400,
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Column(
                            scroll=ft.ScrollMode.ALWAYS,
                            controls=[
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(
                                            label=ft.Text("id", color=ft.Colors.WHITE)
                                        ),
                                        ft.DataColumn(label=ft.Text("fecha",color=ft.Colors.WHITE)),
                                        ft.DataColumn(label=ft.Text("cliente_id",color=ft.Colors.WHITE)),
                                        ft.DataColumn(label=ft.Text("total",color=ft.Colors.WHITE)),
                                        ft.DataColumn(label=ft.Text("estado",color=ft.Colors.WHITE)),
                                    ],
                                    rows=self._obtener_filas(),
                                )
                            ],
                        )
                    ],
                ),
            ],
        )
