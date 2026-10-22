import flet as ft

from shared.ui.components import (
    GlutenNormalText,
    GlutenTextInput,
    GlutenDropdownField,
    GlutenDropdownInput,
    GlutenButton
)


class FormularioVentasComponent(ft.Container):
    def __init__(
        self,
        clientes: list,
        productos: list,
        estados: list,
        on_guardar_venta_click: callable,
    ):
        super().__init__()
        self.clientes = clientes
        self.productos = productos
        self.estados = estados
        self.venta = []
        self.content = self._construir_elementos_formulario()

    def _construir_elementos_formulario(self):
        columna_principal = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        fecha_input := GlutenTextInput(
                            etiqueta="Fecha", pista_texto="Fecha de la venta"
                        ),
                        estado_input := GlutenDropdownInput(
                            pista_texto="estado", etiqueta="Estado", items=self.estados
                        ),
                        cliente_input := GlutenDropdownInput(
                            pista_texto="cliente",
                            etiqueta="Cliente",
                            items=self.clientes,
                        ),
                        productos_input := GlutenDropdownInput(
                            pista_texto="producto",
                            etiqueta="Productos",
                            items=self.productos,
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        boton_registrar := GlutenButton(text='Registar')        
                    ]
                )
            ]
        )
        return columna_principal


# --- BLOQUE DE PRUEBA RÁPIDA DE LA UI 🧪 ---
if __name__ == "__main__":

    def main_test(page: ft.Page):
        page.title = "Prueba Aislada: Formulario Ventas"
        page.bgcolor = ft.Colors.BLACK

        # Callback simulado para verificar qué datos captura el botón
        def callback_simulado(data):
            pass

        # Instanciamos solo el componente que queremos probar
        componente = FormularioVentasComponent(
            clientes=['Maria Vecina piso 1','Rusmilena'],
            productos=['Mini lunchi','Pan trenzado','Pan de masa Madre premium'],
            estados=['Pendiente','Pagado'],
            on_guardar_venta_click=callback_simulado,
        )
        page.add(componente)

    # Lanzas únicamente este componente en ventana
    ft.app(target=main_test)
