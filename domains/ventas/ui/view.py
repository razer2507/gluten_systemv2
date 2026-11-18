import flet as ft

from domains.ventas.repository import PostgresVentasRepository
from domains.ventas.service import VentasService
from domains.ventas.ui.components.formulario import FormularioVentasComponent
from shared.ui.components import GlutenNormalText


class VentasView(ft.Container):
    def __init__(
        self,
        clientes: list[dict],
        productos: list[dict],
        estados: list[dict],
        page: ft.Page,
        service: VentasService,
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
   

# --- BLOQUE DE PRUEBA RÁPIDA DE LA UI  ---
if __name__ == "__main__":

    def main(page: ft.Page):
        page.title = "Prueba Aislada: Formulario Ventas"
        page.bgcolor = ft.Colors.BLACK
        repo_v = PostgresVentasRepository()
        services = VentasService(venta_repo=repo_v, clientes_repo=None)
        ventas_vista = VentasView(
            clientes=[
                {"id": 1, "nombre": "paul ramirez", "referencia": "venecia"},
                {"id": 2, "nombre": "rusmilena", "referencia": "venecia"},
            ],
            productos=[
                {"id": 1, "nombre": "Maxi combo", "categoria": "panaderia"},
                {"id": 2, "nombre": "Mini Lunch", "categoria": "panaderia"},
            ],
            estados=["Pendiente", "Pagado"],
            page=page,
            service=services,
        )
        page.add(ventas_vista)

    # Lanzas únicamente este componente en ventana
    ft.run(main)
