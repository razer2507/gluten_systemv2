import flet as ft


class SideBar(ft.Container):
    def __init__(self,vista_venta:ft.Container,vista_productos:ft.Container, **kwargs):
        super().__init__(**kwargs)
        self.height = 700
        self.tabs = ft.Tabs(
            length=2,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        on_click=self.on_click,
                        tabs=[
                            ft.Tab(label=ft.Text("Ventas",color=ft.Colors.ORANGE_400), icon=ft.Icons.POINT_OF_SALE),
                            ft.Tab(label=ft.Text('Productos',color=ft.Colors.ORANGE_400), icon=ft.Icons.SETTINGS),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=vista_venta,
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=vista_productos,
                            ),
                        ],
                    ),
                ],
            ),
        )

        self.content = self.tabs
