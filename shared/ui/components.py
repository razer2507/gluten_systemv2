import flet as ft

from shared.ui.fonts import fonts
import pdb


class GlutenTextSyle(ft.TextStyle):
    def __init__(self, **kwargs):
        super().__init__(
            font_family=fonts["BebasNeue"], size=24, color=ft.Colors.WHITE, **kwargs
        )


class GlutenNormalText(ft.Text):
    def __init__(self, **kwargs):
        estilo = GlutenTextSyle()
        super().__init__(style=estilo, **kwargs)


class GlutenEntryField(ft.TextField):
    def __init__(self, **kwargs):
        self.estilo = GlutenTextSyle()
        self.estilo.size = 16
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


class GlutenTextInput(ft.Container):
    def __init__(self, etiqueta: str = "Tag", pista_texto: str = "Pista", **kwargs):
        self.etiqueta = etiqueta
        self.pista_texto = pista_texto
        self.spacing = 15
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

    def _construir_input(self) -> ft.Column:
        return ft.Column(
            spacing=self.spacing, controls=[self.etiqueta_texto, self.entrada]
        )


class GlutenDropdownInput(GlutenTextInput):
    def __init__(self, items: list, **kwargs):
        super().__init__(**kwargs)
        self.entrada = GlutenDropdownField(items=items, pista=self.pista_texto)
        self.content = self._construir_input()


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
