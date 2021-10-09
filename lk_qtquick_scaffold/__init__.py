from .application import Application
from .application import app
from .hot_loader import hot_loader
from .pyside import pyside
from .pyside import reg


def _setup():
    from .qlogger import setup as setup_qlogger
    setup_qlogger()
    
    app.register_pyobj(pyside, 'pyside')


_setup()

__version__ = '1.0.0a0'
