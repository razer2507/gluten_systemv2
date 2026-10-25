import flet as ft

from shared.ui.fonts import fonts
import pdb
from datetime import datetime
from dateutil.relativedelta import relativedelta


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

    def construir_opciones(self, items: list) -> list[ft.DropdownOption]:
        return [
            ft.DropdownOption(key=item, content=GlutenNormalText(size=12, value=item))
            for item in items
        ]


class GlutenDatePickerDialog(ft.DatePicker):
    def __init__(
        self,
        start_date: datetime = datetime(year=2024, month=1, day=1),
        end_date: datetime = datetime.now(),
        on_confirmar_fecha: callable() = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.first_date = start_date
        self.last_date = end_date
        self.current_date = datetime.now()
        self.on_change = on_confirmar_fecha


class GlutenDatePickerField(ft.Row):
    def __init__(self, pista: str = "entrada", **kwargs):
        super().__init__(**kwargs)


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
        return self.entrada.value

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
        return self.entrada.value


class GlutenButton(ft.TextButton):
    def __init__(
        self, text: str = "Boton", icon: ft.Icon = ft.Icons.SHOP_2_OUTLINED, **kwargs
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
