try:
    import lk_logger
    lk_logger.setup(quiet=True)
except:
    pass

from .pyside import Application
from .pyside import app
from .pyside import pyside
from .pyside import register
from .pyside import signal
from .pyside import slot
from .qmlside import Model
from .qmlside import eval_js
from .qmlside import hot_loader
from .qmlside import js_eval
from .style import pystyle

__version__ = '2.0.0dev0'


def __setup__():
    """
    register global instances in qml side:
    see also `pyside.list_reserved_pyhandler_names()`.
    """
    from .qmlside import pylayout
    from .qmlside import qlogger
    from .style import pystyle_for_qml
    
    qlogger.setup()
    
    app.register_pyobj(pyside, 'pyside')
    app.register_pyobj(pystyle_for_qml, 'pystyle')
    app.register_pyobj(pystyle.color, 'pycolor')
    app.register_pyobj(pystyle.font, 'pyfont')
    app.register_pyobj(pystyle.motion, 'pymotion')
    app.register_pyobj(pystyle.size, 'pysize')
    app.register_pyobj(pylayout, 'pylayout')


__setup__()
del __setup__
