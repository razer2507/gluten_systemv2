from domains.ventas.ui.components.formulario import FormularioVentasComponent
from domains.ventas.service import VentasService
import flet as ft

class VentasView(ft.Container):
    def __init__(self,page:ft.Page,service:VentasService):
        super().__()
        self.formulario = FormularioVentasComponent(on_guardar_venta_click=self.procesar_venta)
        self.content = self.construir_vista()
        
    def construir_vista(self):
        pass

    def procesar_venta(self):
        pass