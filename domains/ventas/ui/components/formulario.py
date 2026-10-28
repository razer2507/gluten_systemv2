import flet as ft

from shared.ui.components import (
    GlutenButton,
    GlutenDatePickerInput,
    GlutenDropdownInput,
    GlutenProductsPickerField
)
from shared.utils import to_dropdown_option


class FormularioVentasComponent(ft.Container):
    def __init__(
        self,
        pagina_principal: ft.Page,
        clientes: dict | list,
        productos: dict | list,
        estados: dict | list,
        on_guardar_venta_click: callable,
    ):
        super().__init__()
        self.pagina_principal = pagina_principal
        self.clientes = clientes
        self.productos = productos
        self.estados = estados
        self.content = self._construir_elementos_formulario()
        self.on_guardar_venta_click = on_guardar_venta_click

    def _construir_elementos_formulario(self):

        self.fecha_input = GlutenDatePickerInput(
            pagina_principal=self.pagina_principal,
            pista_texto="MM/DD/YY",
            etiqueta="Fecha",
        )
        self.estado_input = GlutenDropdownInput(
            pista_texto="estado", etiqueta="Estado", items=self.estados
        )
        self.cliente_dropdown = GlutenDropdownInput(
            pista_texto="cliente",
            etiqueta="Cliente",
            items=to_dropdown_option(
                keys=[i["id"] for i in self.clientes],
                values=[i["nombre"] for i in self.clientes],
            ),
        )
        self.productos_dropdown = GlutenProductsPickerField(
            pagina_principal=self.pagina_principal,
            productos=self.productos
        )
        self.boton = GlutenButton(text="Registar", on_click=self._procesar_venta)

        columna_principal = ft.Column(
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        self.estado_input,
                        self.cliente_dropdown,
                        self.productos_dropdown,
                        self.fecha_input,
                    ],
                ),
                ft.Row(controls=self.boton),
            ]
        )

        return columna_principal

    def _procesar_venta(self):
        self.on_guardar_venta_click(
            {
                "fecha": self.fecha_input.valor,
                "estado": self.estado_input.valor,
                "cliente": self.cliente_dropdown.valor,
                "productos": self.productos_dropdown.valor,
            }
        )


# --- BLOQUE DE PRUEBA RÁPIDA DE LA UI 🧪 ---
if __name__ == "__main__":

    def main_test(page: ft.Page):
        page.title = "Prueba Aislada: Formulario Ventas"
        page.bgcolor = ft.Colors.BLACK

        # Callback simulado para verificar qué datos captura el botón
        def callback_simulado(data):
            print(f"venta con datos {data} GUARDADA CON EXITO.")

        # Instanciamos solo el componente que queremos probar
        componente = FormularioVentasComponent(
            pagina_principal=page,
            clientes=[
                {"id": 1, "nombre": "paul ramirez", "referencia": "venecia"},
                {"id": 2, "nombre": "rusmilena", "referencia": "venecia"},
            ],
            productos=[
                {"id": 1, 'nombre': 'Maxi combo', 'categoria': 'panaderia'},
                {'id':2,'nombre':'Mini Lunch','categoria':'panaderia'}
            ],
            estados=["Pendiente", "Pagado"],
            on_guardar_venta_click=callback_simulado,
        )
        page.add(componente)

    # Lanzas únicamente este componente en ventana
ft.app(target=main_test)


# TODO:creacion de fecha dialog, y envio de datos a servicio de ventas
