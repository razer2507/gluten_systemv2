from datetime import datetime
from uuid import uuid4

import pytest

from config.settings import DatabaseSettings
from domains.gastos.infrastructure.postgres_repo import (
    PostgresGastosRepository,
)
from domains.gastos.models import Gasto

repo = PostgresGastosRepository(DatabaseSettings.test_from_env())


def _gasto(categoria: str | None = None, monto: float = 10.5) -> Gasto:
    return Gasto(
        categoria=categoria or f"test-{uuid4().hex}",
        monto=monto,
        fecha=datetime(2026, 1, 1, 12, 0, 0),
        descripcion="gasto de prueba",
        tipo="Test",
    )


def test_insert_y_get_by_id():
    gasto = _gasto()
    gasto_id = repo.insert(gasto)
    try:
        assert gasto_id is not None
        data = repo.get_by_id(gasto_id)
        assert data is not None
        assert data.id == gasto_id
        assert data.categoria == gasto.categoria
        assert data.monto == pytest.approx(gasto.monto)
        assert data.fecha == gasto.fecha
        assert data.descripcion == gasto.descripcion
        assert data.tipo == gasto.tipo
    finally:
        repo.delete(Gasto(categoria=gasto.categoria, monto=0, id=gasto_id))


def test_get_all():
    data = repo.get_all()
    assert isinstance(data, list)
    assert all(isinstance(item, Gasto) for item in data)


def test_get_by_id_inexistente_retorna_none():
    assert repo.get_by_id(-1) is None


def test_get_filtered_por_categoria_y_monto():
    categoria = f"cat-{uuid4().hex}"
    gasto_id = repo.insert(_gasto(categoria=categoria, monto=25.5))
    try:
        data = repo.get_filtered(categoria=categoria, monto_min=20)
        assert len(data) >= 1
        assert all(item.categoria == categoria for item in data)
        assert all(item.monto >= 20 for item in data)
    finally:
        repo.delete(Gasto(categoria=categoria, monto=0, id=gasto_id))


def test_update():
    gasto_id = repo.insert(_gasto())
    try:
        actualizado = repo.get_by_id(gasto_id)
        actualizado.monto = 99.5
        actualizado.descripcion = "descripcion actualizada"
        actualizado.tipo = "Variable"

        repo.update(actualizado)

        data = repo.get_by_id(gasto_id)
        assert data.monto == pytest.approx(actualizado.monto)
        assert data.descripcion == actualizado.descripcion
        assert data.tipo == actualizado.tipo
    finally:
        repo.delete(Gasto(categoria=actualizado.categoria, monto=0, id=gasto_id))


def test_delete():
    gasto = _gasto()
    gasto_id = repo.insert(gasto)

    repo.delete(Gasto(categoria=gasto.categoria, monto=0, id=gasto_id))

    assert repo.get_by_id(gasto_id) is None
