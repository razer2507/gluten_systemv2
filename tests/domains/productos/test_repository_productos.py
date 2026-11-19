from uuid import uuid4

import pytest

from config.settings import DatabaseSettings
from domains.productos.models import Producto
from domains.productos.repository import PostgresProductosRepository

repo = PostgresProductosRepository(DatabaseSettings.test_from_env())


def _producto(nombre: str | None = None, categoria: str = "test_categoria") -> Producto:
    return Producto(
        nombre=nombre or f"test-{uuid4().hex}",
        precio_costo=1.5,
        categoria=categoria,
    )


def test_insert_y_get_by_id():
    producto = _producto()
    producto_id = repo.insert(producto)
    try:
        assert producto_id is not None
        data = repo.get_by_id(producto_id)
        assert data is not None
        assert data.id == producto_id
        assert data.nombre == producto.nombre
        assert data.precio_costo == pytest.approx(producto.precio_costo)
        assert data.categoria == producto.categoria
    finally:
        repo.delete(Producto(id=producto_id))


def test_get_all():
    data = repo.get_all()
    assert isinstance(data, list)
    assert all(isinstance(item, Producto) for item in data)


def test_get_by_id_inexistente_retorna_none():
    assert repo.get_by_id(-1) is None


def test_get_filtered_por_categoria():
    categoria = f"cat-{uuid4().hex}"
    producto_id = repo.insert(_producto(categoria=categoria))
    try:
        data = repo.get_filtered(categoria=categoria)
        assert len(data) >= 1
        assert all(item.categoria == categoria for item in data)
    finally:
        repo.delete(Producto(id=producto_id))


def test_update():
    producto_id = repo.insert(_producto())
    try:
        actualizado = repo.get_by_id(producto_id)
        actualizado.nombre = f"actualizado-{uuid4().hex}"
        actualizado.precio_costo = 9.99

        repo.update(actualizado)

        data = repo.get_by_id(producto_id)
        assert data.nombre == actualizado.nombre
        assert data.precio_costo == pytest.approx(actualizado.precio_costo)
    finally:
        repo.delete(Producto(id=producto_id))


def test_delete():
    producto_id = repo.insert(_producto())

    repo.delete(Producto(id=producto_id))

    assert repo.get_by_id(producto_id) is None
