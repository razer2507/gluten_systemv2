import flet as ft

from shared.ui.fonts import fonts


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
        super().__init__(
            text_style=self.estilo,
            bgcolor=ft.Colors.TRANSPARENT,
            filled=False,
            border=ft.InputBorder.NONE,
            **kwargs,
        )


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

    def _construir_input(self):
        return ft.Column(
            spacing=self.spacing, controls=[self.etiqueta_texto, self.entrada]
        )
