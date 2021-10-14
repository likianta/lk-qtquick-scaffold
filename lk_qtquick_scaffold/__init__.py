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
        from .qmlside import qlogger
        qlogger.setup()
        
        from .qmlside import LayoutHelper
        app.register_pyobj(pyside, 'pyside')
        app.register_pyobj(pyside, 'PySide')
        app.register_pyobj(LayoutHelper(), 'LKLayoutHelper')
        
        from .qmlside import resource_manager as rm
        app.register_pyobj(rm.AssetsResourceManager(), 'RMAssets')
        app.register_pyobj(rm.ColorResourceManager(), 'RMColor')
        app.register_pyobj(rm.ControlResourceManager(), 'RMControl')
        app.register_pyobj(rm.LayoutResourceManager(), 'RMLayout')
        app.register_pyobj(rm.MotionResourceManager(), 'RMMotion')
        app.register_pyobj(rm.ShapeResourceManager(), 'RMShape')
        app.register_pyobj(rm.TextResourceManager(), 'RMText')
    
    
    _setup()
finally:
    del _setup

__version__ = '1.0.0'
