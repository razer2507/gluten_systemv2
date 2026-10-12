import flet as ft

from shared.ui.fonts import fonts


class GlutenNormalText(ft.Text):
    def __init__(self,texto:str = 'texto',**kwargs):
        super().__init__(
            value=texto,
            font_family=fonts['BebasNeue'],
            size=24,
            color=ft.Colors.WHITE,
            **kwargs
        )
        