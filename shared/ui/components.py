from datetime import datetime

import flet as ft

from shared.ui.fonts import fonts
from shared.utils import to_dropdown_option


class GlutenTextSyle(ft.TextStyle):
    def __init__(self, **kwargs):
        super().__init__(
            font_family=fonts["BebasNeue"], size=14, color=ft.Colors.WHITE, **kwargs
        )


class GlutenNormalText(ft.Text):
    def __init__(self, **kwargs):
        estilo = GlutenTextSyle()
        super().__init__(style=estilo, **kwargs)


class GlutenEntryField(ft.TextField):
    def __init__(self, **kwargs):
        self.estilo = GlutenTextSyle()
        super().__init__(
            text_style=self.estilo,
            bgcolor=ft.Colors.TRANSPARENT,
            filled=False,
            border_color=ft.Colors.ORANGE_400,
            **kwargs,
        )

    @property
    def valor(self):
        return self.value


class GlutenDropdownField(ft.Dropdown):
    def __init__(self, pista: str, items: list, **kwargs):
        super().__init__(
            text_style=GlutenTextSyle(),
            width=250,
            border_color=ft.Colors.ORANGE_400,
            enable_filter=True,
            label=pista,
            bgcolor=ft.Colors.BLACK,
            color=ft.Colors.WHITE,
            **kwargs,
        )
        self.options = self.construir_opciones(items)

    def construir_opciones(self, items: list(tuple) | list) -> list[ft.DropdownOption]:
        if isinstance(items, list) and all(isinstance(i, tuple) for i in items):
            return [
                ft.DropdownOption(
                    key=item[0], content=GlutenNormalText(size=12, value=item[1])
                )
                for item in items
            ]
        else:
            return [
                ft.DropdownOption(
                    key=item, content=GlutenNormalText(size=12, value=item)
                )
                for item in items
            ]

    @property
    def valor(self):
        return self.value


class GlutenDatePickerDialog(ft.DatePicker):
    def __init__(
        self,
        start_date: datetime = datetime(year=2024, month=1, day=1),
        end_date: datetime = datetime.now(),  # noqa: B008
        on_confirmar_fecha: callable() = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.first_date = start_date
        self.last_date = end_date
        self.current_date = datetime.now()
        self.on_change = on_confirmar_fecha


class GlutenProductsDialog(ft.AlertDialog):
    def __init__(
        self,
        productos: list(dict),
        titulo: str = "Elija a continuacion los productos ",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.productos = productos
        self.entrada = GlutenDropdownInput(
            items=to_dropdown_option(
                keys=[i["id"] for i in self.productos],
                values=[i["nombre"] for i in self.productos],
            )
        )
        self.productos_seleccionados = []
        self.modal = True
        self.content = self._construir_formulario_productos()
        self.actions = [
            ft.TextButton(
                "Agregar Producto", style=GlutenTextSyle(), on_click=lambda e: self._agregar_producto()
            )
        ]

    def _construir_formulario_productos(self):
        self.fila_1 = ft.Row(controls=self.entrada)
        self.fila_2 = ft.Column(controls=[])
        columna_principal = ft.Column(controls=[self.fila_1,self.fila_2])
        return columna_principal

    def _agregar_producto(self):
        self.productos_seleccionados.append({
            'id_producto':self.entrada.valor
        })
        self.fila_2.controls.append(ft.Row(
            controls=[ft.Text(self.entrada.valor),ft.Text('Producto')]
        ))

class GlutenDatePickerField(ft.Row):
    def __init__(self, pagina_principal: ft.Page, pista: str = "entrada", **kwargs):
        super().__init__(**kwargs)
        self.pagina_principal = pagina_principal
        self.entrada = GlutenEntryField(hint_text=pista, width=200, read_only=True)
        self.dialog_fecha = GlutenDatePickerDialog(
            on_confirmar_fecha=self.on_click_fecha
        )
        self.boton_fecha = ft.IconButton(
            ft.Icons.DATE_RANGE,
            icon_color=ft.Colors.ORANGE_400,
            on_click=lambda _: self.pagina_principal.show_dialog(self.dialog_fecha),
        )
        self.spacing = 1
        self.controls = [self.entrada, self.boton_fecha]

    def on_click_fecha(self, e: ft.Event[ft.DatePicker]) -> None:
        self.entrada.value = e.control.value.strftime("%m/%d/%Y")

    @property
    def valor(self) -> ft.TextField.value:
        return self.entrada.value

class GlutenProductsPickerField(ft.Row):
    def __init__(self, pagina_principal: ft.Page,productos:list[dict],pista: str = "entrada", **kwargs):
        super().__init__(**kwargs)
        self.pagina_principal = pagina_principal
        self.entrada = GlutenEntryField(hint_text=pista, width=200, read_only=True)
        self.dialog_productos = GlutenProductsDialog(productos=productos)
        self.boton_add = ft.IconButton(
            ft.Icons.ADD,
            icon_color=ft.Colors.ORANGE_400,
            on_click=lambda _: self.pagina_principal.show_dialog(self.dialog_productos),
        )
        self.spacing = 1
        self.controls = [self.entrada, self.boton_add]

    @property
    def valor(self) -> ft.TextField.value:
        return self.entrada.value


class GlutenTextInput(ft.Container):
    def __init__(self, etiqueta: str = "Tag", pista_texto: str = "Pista", **kwargs):
        self.etiqueta = etiqueta
        self.pista_texto = pista_texto
        self.spacing = 16
        super().__init__(
            width=150,
            height=150,
            alignment=ft.Alignment.CENTER,
            bgcolor=ft.Colors.TRANSPARENT,
            **kwargs,
        )
        self.etiqueta_texto = GlutenNormalText(
            value=self.etiqueta, color=ft.Colors.ORANGE_400
        )
        self.entrada = GlutenEntryField(hint_text=self.pista_texto)
        self.content = self._construir_input()

    @property
    def valor(self):
        return self.entrada.valor

    def _construir_input(self) -> ft.Column:
        return ft.Column(
            spacing=self.spacing, controls=[self.etiqueta_texto, self.entrada]
        )


class GlutenDropdownInput(GlutenTextInput):
    def __init__(self, items: list, **kwargs):
        super().__init__(**kwargs)
        self.entrada = GlutenDropdownField(items=items, pista=self.pista_texto)
        self.content = self._construir_input()

    @property
    def valor(self):
        return self.entrada.valor


class GlutenDatePickerInput(GlutenTextInput):
    def __init__(self, pagina_principal: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.entrada = GlutenDatePickerField(
            pagina_principal=pagina_principal, pista=self.pista_texto
        )
        self.content = self._construir_input()
        self.width = 250

    def _construir_input(self):
        return ft.Column(
            spacing=self.spacing, controls=[self.etiqueta_texto, self.entrada]
        )

    @property
    def valor(self):
        return self.entrada.valor


class GlutenButton(ft.TextButton):
    def __init__(
        self, text: str = "Boton", icon: ft.Icon = ft.Icons.CHECK_OUTLINED, **kwargs
    ):
        self.texto_boton = text
        super().__init__(
            content=GlutenNormalText(value=self.texto_boton, color=ft.Colors.WHITE),
            icon=icon,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_900,
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                },
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            **kwargs,
        )
