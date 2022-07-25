if 1:  # step1: setup lk_logger
    import lk_logger
    lk_logger.setup(quiet=True)

if 2:  # step2: select qt api
    # this should be defined before importing qtpy.
    # refer: [lib:qtpy/__init__.py : docstring]
    import os
    from importlib.util import find_spec
    
    api = ''
    if not os.getenv('QT_API'):
        for pkg, api in {
            'PySide6': 'pyside6',
            'PyQt6'  : 'pyqt6',
            'PySide2': 'pyside2',
            'PyQt5'  : 'pyqt5',
        }.items():
            if find_spec(pkg):
                print(':v2', 'Auto detected Qt API: ' + api)
                os.environ['QT_API'] = api
                break
        else:
            raise ModuleNotFoundError('No Qt bindings found!')
    
    if api == 'pyside2':
        # try to repair pyside2 highdpi issue
        #   https://www.hwang.top/post/pyside2pyqt-zai-windows-zhong-tian-jia
        #       -dui-gao-fen-ping-de-zhi-chi/
        # warning: this must be called before QCoreApplication is created.
        from PySide2 import QtCore  # noqa
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

# -----------------------------------------------------------------------------

from .application import Application
from .application import app
from .pyside import pyside
from .pyside import register
from .qmlside import Model
from .qmlside import eval_js
from .qmlside import js_eval
from .qt_core import QObject
from .qt_core import signal
from .qt_core import slot
from .style import pystyle

__version__ = '2.0.0'


def __setup__():
    """
    register global instances in qml side:
    see also `pyside.list_reserved_pyhandler_names()`.
    """
    from .qmlside import pylayout
    from .qmlside import qlogger
    from .qmlside import widgets_backend
    from .style import pystyle_for_qml
    
    qlogger.setup(ignore_unpleasent_warnings=True)
    widgets_backend.init(app)
    
    app.register_pyobj(pyside, 'pyside')
    app.register_pyobj(pystyle_for_qml, 'pystyle')
    app.register_pyobj(pystyle.color, 'pycolor')
    app.register_pyobj(pystyle.font, 'pyfont')
    app.register_pyobj(pystyle.motion, 'pymotion')
    app.register_pyobj(pystyle.size, 'pysize')
    app.register_pyobj(pylayout, 'pylayout')


__setup__()
del __setup__
