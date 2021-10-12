from .pyside import Application
from .pyside import app
from .pyside import pyside
from .pyside import reg
from .qmlside import hot_loader
from .qmlside import eval_js
from .qmlside import js_eval


def _setup():
    from .qmlside import LKLayoutHelper
    from .qmlside import qlogger
    qlogger.setup()
    app.register_pyobj(pyside, 'pyside')
    app.register_pyobj(pyside, 'PySide')
    app.register_pyobj(LKLayoutHelper(), 'LKLayoutHelper')


_setup()

__version__ = '1.0.0a0'
