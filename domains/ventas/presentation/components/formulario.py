import asyncio

import flet as ft

from domains.ventas.domain_services.strategies import CanalFactory
from shared.ui.components import (
    GlutenButton,
    GlutenDatePickerInput,
    GlutenDropdownInput,
    GlutenProductsPickerInput,
)
from shared.utils import to_dropdown_option


class FormularioVentasComponent(ft.Container):
    def __init__(
        self,
        pagina_principal: ft.Page,
        clientes,
        productos,
        estados,
        on_guardar_venta_click: callable(),
    ):
        super().__init__()
        self.pagina_principal = pagina_principal
        self.clientes = clientes
        self.productos = productos
        self.estados = estados
        self.canales = CanalFactory()
        self.content = self._construir_elementos_formulario()
        self.on_guardar_venta_click = on_guardar_venta_click
        self.border = ft.Border.all(color=ft.Colors.ORANGE_400)
        self.width = 900
        self.height = 500

    def _construir_elementos_formulario(self):
        self.fecha_input = GlutenDatePickerInput(
            pagina_principal=self.pagina_principal,
            pista_texto="MM/DD/YY",
            etiqueta="Fecha",
        )
        self.estado_input = GlutenDropdownInput(
            pista_texto="Contado o Credito?", etiqueta="Estado", items=['contado','credito']
        )
        self.cliente_dropdown = GlutenDropdownInput(
            pista_texto="Elegir un cliente",
            etiqueta="Cliente",
            items=[
                ft.DropdownOption(
                    key=str(cliente["id"]),
                    text=cliente["nombre"],
                )
                for cliente in self.clientes
            ]
        )
        self.canal_dropdown = GlutenDropdownInput(
            items=list(self.canales.canales.keys()),
            etiqueta="Canal de Venta",
            pista_texto="Elegir Canal de Venta",
        )
        self.boton = GlutenButton(text="Registar Venta", on_click=self._procesar_venta)

        columna_principal = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        self.cliente_dropdown,
                        self.canal_dropdown
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[self.estado_input, self.fecha_input],
                ),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=self.boton),
            ],
        )

        return columna_principal

    async def _procesar_venta(self):
        success = True
        try:
            res_id = self.on_guardar_venta_click(
                {
                    "fecha": self.fecha_input.valor,
                    "estado": self.estado_input.valor,
                    "cliente_id": self.cliente_dropdown.valor,
                    "canal": self.canal_dropdown.valor,
                }
            )
            msg = f"Venta Registrada con exito ID {res_id}"
        except Exception:  # noqa: BLE001
            msg = "Error al registrar la venta"
            success = False
        finally:
            color = ft.Colors.GREEN_700 if success else ft.Colors.RED_700
            icon = ft.Icons.CHECK if success else ft.Icons.DANGEROUS
            mensaje = ft.Banner(
                leading=ft.Icon(icon,color=color),
                content=ft.Text(msg,color=color),
                actions=[ft.TextButton("Aceptar",on_click= lambda _ : self.pagina_principal.pop_dialog())],
                bgcolor=ft.Colors.BLACK,
                open=True,
            )
            self.pagina_principal.show_dialog(mensaje)
            await asyncio.sleep(2)
            self.pagina_principal.pop_dialog()

            if success:
                self.fecha_input.limpiar_entrada()
                self.estado_input.limpiar_entrada()
                self.cliente_dropdown.limpiar_entrada()
                self.canal_dropdown.limpiar_entrada()
                self.content.update()
