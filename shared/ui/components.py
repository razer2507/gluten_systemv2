from datetime import datetime

import flet as ft

from shared.ui.fonts import fonts
from shared.utils import to_dropdown_option


class GlutenTextSyle(ft.TextStyle):
    def __init__(self, size: int = 14, **kwargs):
        super().__init__(
            font_family=fonts["BebasNeue"], color=ft.Colors.WHITE, **kwargs
        )
        self.size = size


class GlutenNormalText(ft.Text):
    def __init__(self, **kwargs):
        estilo = GlutenTextSyle()
        super().__init__(style=estilo, **kwargs)

    @property
    def valor(self):
        return self.value


class GlutenEntryField(ft.TextField):
    def __init__(self, size_text: int = 14, **kwargs):
        self.estilo = GlutenTextSyle(size=size_text)
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
        actualizar_total: callable(),
        pagina_principal: ft.Page,
        productos: list(dict),
        titulo: str = "Elija a continuacion los productos ",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.bgcolor = ft.Colors.BLACK
        self.pagina_principal = pagina_principal
        self.productos = productos
        self.entrada = GlutenDropdownInput(
            items=to_dropdown_option(
                keys=[i["id"] for i in self.productos],
                values=[i["nombre"] for i in self.productos],
            ),
            etiqueta="Productos",
            pista_texto="Elegir Productos",
            on_select=self._agregar_producto,
        )
        self.productos_vendidos = []
        self.productos_seleccionados_ids = []
        self.modal = True
        self.content = self._construir_formulario_productos()
        self.actions = [
            ft.TextButton(
                "Cerrar",
                style=GlutenTextSyle(),
                on_click=lambda e: [
                    self._obtener_data_productos_seleccionados(),
                    self.pagina_principal.pop_dialog(),
                ],
            )
        ]
        self.actualizar_total = actualizar_total

    def _construir_formulario_productos(self):
        self.fila_1 = ft.Row(controls=self.entrada)
        self.fila_2 = ft.DataTable(
            columns=[
                ft.DataColumn(label=GlutenNormalText(value="id")),
                ft.DataColumn(label=GlutenNormalText(value="nombre")),
                ft.DataColumn(label=GlutenNormalText(value="cantidad")),
                ft.DataColumn(label=GlutenNormalText(value="precio_unitario")),
            ],
            rows=[],
        )
        columna_principal = ft.Column(width=500, controls=[self.fila_1, self.fila_2])
        return columna_principal

    def _buscar_producto_por_id(self, id: int) -> str:
        for producto in self.productos:
            if producto["id"] == int(id):
                return producto

    def _calcular_total(self):
        suma = float(
            sum(
                [
                    float(producto["cantidad"]) * float(producto["precio_unitario"])
                    for producto in self.productos_vendidos
                ]
            )
        )
        return suma

    def _obtener_data_productos_seleccionados(self):
        cols = [i.label for i in self.fila_2.columns]
        for row in self.fila_2.rows:
            row_data = {}
            for col, cell in zip(cols, row.cells):
                row_data[col.valor] = cell.content.valor
            if not self.producto_es_duplicado(id=int(row_data["id"])):
                self.productos_vendidos.append(row_data)
        self.actualizar_total(self._calcular_total())

    def producto_es_duplicado(self, id) -> bool:
        if id in [producto["id"] for producto in self.productos_vendidos]:
            return True

    def _producto_ha_sido_seleccionado(self, id_producto: int) -> bool:
        if id_producto in self.productos_seleccionados_ids:
            return True

    def _agregar_producto(self, e: ft.Event[ft.Dropdown]) -> None:
        if self._producto_ha_sido_seleccionado(id_producto=int(e.control.value)):
            return
        producto = self._buscar_producto_por_id(id=int(e.control.value))
        self.productos_seleccionados_ids.append(producto["id"])
        self._agregar_data_tabla(id=producto["id"], nombre=producto["nombre"])

    def _agregar_data_tabla(self, id, nombre) -> None:
        self.fila_2.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(GlutenNormalText(value=id)),
                    ft.DataCell(GlutenNormalText(value=nombre)),
                    ft.DataCell(
                        GlutenEntryField(
                            hint_text="cantidad", width=80, height=35, size_text=12
                        )
                    ),
                    ft.DataCell(
                        GlutenEntryField(
                            hint_text="precio unitario",
                            width=80,
                            height=35,
                            size_text=12,
                        )
                    ),
                ]
            )
        )


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
    def __init__(
        self,
        actualizar_total: callable(),
        pagina_principal: ft.Page,
        productos: list[dict],
        pista: str = "entrada",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.pagina_principal = pagina_principal
        self.entrada = GlutenEntryField(hint_text=pista, width=200, read_only=True)
        self.dialog_productos = GlutenProductsDialog(
            actualizar_total=actualizar_total,
            pagina_principal=self.pagina_principal,
            productos=productos,
        )
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
    def __init__(self, items: list, on_select: callable() = None, **kwargs):
        super().__init__(**kwargs)
        self.entrada = GlutenDropdownField(
            on_select=on_select, items=items, pista=self.pista_texto
        )
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

    def _construir_input(self) -> ft.Column:
        return ft.Column(
            spacing=self.spacing, controls=[self.etiqueta_texto, self.entrada]
        )

    @property
    def valor(self):
        return self.entrada.valor


class GlutenProductsPickerInput(GlutenTextInput):
    def __init__(self, pagina_principal: ft.Page, productos: list(dict), **kwargs):
        self.pagina_principal = pagina_principal
        super().__init__(**kwargs)
        self.entrada = GlutenProductsPickerField(
            pagina_principal=self.pagina_principal,
            productos=productos,
            pista=self.pista_texto,
            actualizar_total=self.actualizar_total
        )
        self.width = 235
        self.content = self._construir_input()

    def _construir_input(self) -> ft.Column:
        return ft.Column(
            spacing=self.spacing, controls=[self.etiqueta_texto, self.entrada]
        )

    def actualizar_total(self, total: float):
        self.entrada.entrada.value = total


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
