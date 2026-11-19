from app.ctx import AppContext
from config.settings import DatabaseSettings
from domains.ventas.ui.view import VentasView
if __name__ == '__main__':
    ctx = AppContext(settings=DatabaseSettings.test_from_env())
    ventas_view = VentasView()