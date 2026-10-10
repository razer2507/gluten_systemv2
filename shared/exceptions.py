class VentasDomainError(Exception):
    """Excepción base para el dominio de ventas."""

class VentaSinProductosError(VentasDomainError):
    """Se lanza cuando se intenta registrar una venta sin ítems."""
    def __init__(self, mensaje: str = "Los productos de la venta no son validos"):
        super().__init__(mensaje)


class FechaInvalidaError(VentasDomainError):
    def __init__(self, mensaje: str = "La fecha seleccionada no es valida"):
        super().__init__(mensaje)

class ClienteInvalidoError(VentasDomainError):
    """Se lanza cuando el cliente asociado no es válido."""
    def __init__(self, mensaje: str = "El cliente seleccionado no es válido."):
        super().__init__(mensaje)

class EstadoInvalidoError(VentasDomainError):
    def __init__(self,mensaje: str = "El estado de la venta es invalido"):
        super().__init__(mensaje)

class TotalInvalidoError(VentasDomainError):
    def __init__(self,mensaje: str = "El total de la venta es invalido"):
        super().__init__(mensaje)

class CanalInvalidoError(VentasDomainError):
    def __init__(self,mensaje : str = "El canal de la venta es invalido"):
        super().__init__(mensaje)