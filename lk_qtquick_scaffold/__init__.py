from .pyside import Application
from .pyside import app
from .pyside import pyside
from .pyside import reg
from .qmlside import adapt_argtypes
from .qmlside import eval_js
from .qmlside import hot_loader
from .qmlside import js_eval

try:
    def _setup():
        from .qmlside import LayoutHelper
        from .qmlside import qlogger
        qlogger.setup()
        app.register_pyobj(pyside, 'pyside')
        app.register_pyobj(pyside, 'PySide')
        app.register_pyobj(LayoutHelper(), 'LKLayoutHelper')
    
    
    _setup()
finally:
    del _setup

__version__ = '1.0.0a0'
