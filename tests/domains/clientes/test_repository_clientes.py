from domains.clientes.models import Cliente
from domains.clientes.repository import PostgresClientesRepository

repo = PostgresClientesRepository()

def test_insert_cliente():
    cliente = Cliente(nombre="Juan Perez", referencia="ref123")
    cliente_id = repo.insert(cliente)
    assert cliente_id is not None
    
    data = repo.get_by_id(cliente_id)
    assert data is not None
    assert data.id == cliente_id
    assert data.nombre == cliente.nombre
    assert data.referencia == cliente.referencia

def test_get_all_cliente():
    data = repo.get_all()
    assert isinstance(data, list)
    assert all(isinstance(x, Cliente) for x in data)

def test_get_by_id_cliente():
    cliente = Cliente(nombre="Maria Gomez", referencia="ref456")
    cliente_id = repo.insert(cliente)
    
    data = repo.get_by_id(cliente_id)
    assert data is not None
    assert data.id == cliente_id
    assert data.nombre == "Maria Gomez"

def test_update_cliente():
    cliente = Cliente(nombre="Pedro", referencia="ref789")
    cliente_id = repo.insert(cliente)
    
    cliente_para_actualizar = repo.get_by_id(cliente_id)
    cliente_para_actualizar.nombre = "Pedro Actualizado"
    
    repo.update(cliente_para_actualizar)
    
    data = repo.get_by_id(cliente_id)
    assert data.nombre == "Pedro Actualizado"

def test_delete_cliente():
    cliente = Cliente(nombre="Eliminar", referencia="ref000")
    cliente_id = repo.insert(cliente)
    
    repo.delete(repo.get_by_id(cliente_id))
    
    assert repo.get_by_id(cliente_id) is None
