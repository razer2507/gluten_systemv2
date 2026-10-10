from datetime import date

from domains.ventas.models import DetalleVenta, Venta
from domains.ventas.repository import PostgresVentasRepository

repo = PostgresVentasRepository()


def test_insert():

    venta_fake = Venta(
        fecha="2026-08-08",
        cliente_id=1,
        total=20,
        productos=[
            DetalleVenta(producto_id=1, cantidad=2, precio_unitario=2.5),
            DetalleVenta(producto_id=3, cantidad=4, precio_unitario=2.5),
        ],
        estado="pagado",
    )
    id_venta = repo.insert(venta_fake)
    print(repo.get_by_id(id_venta))
    data = repo.get_by_id(id_venta)
    assert data is not None
    assert data.id == id_venta
    assert data.fecha == date.fromisoformat(venta_fake.fecha)
    assert data.cliente_id == venta_fake.cliente_id
    assert data.total == venta_fake.total
    assert data.estado == venta_fake.estado


def test_get_all():

    data = repo.get_all()
    assert len(data) > 0
    assert all(isinstance(x, Venta) for x in data)


def test_get_by_id():
    venta_id_a_buscar = 1
    data = repo.get_by_id(venta_id_a_buscar)
    assert data.id == venta_id_a_buscar


def test_filter():
    args = {"total_max": 20, "estado": "pagado"}

    def comprobar_fecha(fecha):
        return bool(
            isinstance(fecha, date)
            and (
                fecha >= date.fromisoformat(args["fecha_inicio"])
                and fecha <= date.fromisoformat(args["fecha_fin"])
            )
        )

    def comprobar_estado(estado):
        return bool(args["estado"] == estado)

    def comprobar_total(total):
        return bool(int(total) in range(args.get("total_min"), args.get("total_max")))

    data = repo.get_filtered(**args)
    assert data is not None
    if args.get("fecha_fin") and args.get("fecha_inicio"):
        assert all(comprobar_fecha(venta.fecha) for venta in data)
    if args.get("estado"):
        assert all(comprobar_estado(venta.estado) for venta in data)
    if args.get("total_min") and args.get("total_max"):
        assert all(comprobar_total(venta.total) for venta in data)


def test_update():
    venta_original = Venta(
        fecha="2026-08-08",
        total=3500,
        estado="en deuda",
        cliente_id=17,
        productos=[DetalleVenta(producto_id=1, cantidad=5, precio_unitario=2.5)],
    )
    # 1- Inserto la venta y devuelvo el id
    venta_original_id = repo.insert(venta_original)
    venta_original.id = venta_original_id
    # 2- Consigo el objeto venta recien insertado usando el metodo obtener por id
    venta_nueva = repo.get_by_id(venta_original_id)
    # 3- Modifico la venta anteriormente insertada
    venta_nueva.fecha = "2025-08-08"
    venta_nueva.total = 4500.0
    # 4- Sobreescribo los datos y luego los actualizado usando  el metodo update
    repo.update(venta_nueva)
    # 5- obtengo nuevamente el objeto venta ya actualizado
    venta_luego_de_actualizar = repo.get_by_id(venta_original_id)
    # 6 - Comparacion (Los datos que se querian cambiar vs los datos reales luego de la operacion UPDATE)
    assert venta_luego_de_actualizar.fecha == date.fromisoformat(venta_nueva.fecha)
    assert venta_luego_de_actualizar.total == venta_nueva.total


def test_delete():
    venta_nueva = Venta(
        fecha="2025-08-07",
        total=6500,
        estado="pagado",
        cliente_id=17,
        productos=[
            DetalleVenta(producto_id=1, cantidad=2, precio_unitario=2.5),
            DetalleVenta(producto_id=3, cantidad=4, precio_unitario=2.5),
        ],
    )
    venta_id = repo.insert(venta_nueva)
    repo.delete(repo.get_by_id(venta_id))

    assert  (repo.get_by_id(venta_id)) is None
