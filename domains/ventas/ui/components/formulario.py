import flet as ft

from shared.ui.components import GlutenNormalText,GlutenTextInput


class FormularioVentasComponent(ft.Container):
    def __init__(self,on_guardar_venta_click:callable):
        super().__init__()
        self.venta = []
        self.content = self._construir_elementos_formulario()
    
    def _construir_elementos_formulario(self):
        columna_principal = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        GlutenTextInput(etiqueta='Fecha'),
                        GlutenTextInput(etiqueta='Estado')
                    ]
                )
            ]
        )
        return columna_principal



#--- BLOQUE DE PRUEBA RÁPIDA DE LA UI 🧪 ---
if __name__ == "__main__":
    def main_test(page: ft.Page):
        page.title = "Prueba Aislada: Formulario Ventas"
        page.bgcolor = ft.Colors.BLACK
        
        # Callback simulado para verificar qué datos captura el botón
        def callback_simulado(data):
            pass
        # Instanciamos solo el componente que queremos probar
        componente = FormularioVentasComponent(on_guardar_venta_click=callback_simulado)
        page.add(componente)

    # Lanzas únicamente este componente en ventana
    ft.app(target=main_test)