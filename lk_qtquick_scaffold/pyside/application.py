import os.path as xpath

from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import QQmlContext
from PySide6.QtWidgets import QApplication

from ..path_model import theme_dir
from ..typehint import Dict
from ..typehint import TPath


class _Application(QApplication):
    engine: QQmlApplicationEngine
    root: QQmlContext
    
    # the holder is made for preventing the objects which were registered to
    # qml side from being recycled by python garbage collector incorrectly.
    __pyobj_holder: Dict[str, QObject]
    
    def __init__(self, app_name='LK QtQuick Scaffold App', **kwargs):
        """
        Args:
            app_name: str
                Set application name now or later by calling `Application
                .set_app_name(...)`.
            kwargs:
                organization: str['lib.declare_pyside']
                    Set an organization name, to avoid error info when we use
                    `QtQuick.Dialogs.FileDialog`.
                    Note: if no organization name set, the error message shows:
                        QML Settings: The following application identifiers
                        have not been set: QVector("organizationName",
                        "organizationDomain")
                theme_dir: str[`../theme`]
                    You can pass a custom dir which includes themes. Otherwise
                    declare-qml will use its built-in themes (the widely used
                    and maintained is 'LightClean' theme).
                    The theme dir structure should be like this:
                        D:/workspace/xxx
                        |= custom_theme       # pass this to kwargs['theme_dir']
                            |= MaterialTheme  # use big camel case
                                |- MText.qml
                                |- MRectangle.qml
                                |- ...
                                |- qmldir     # don't forget this file
                            |= OceanTheme
                            |= BootstrapTheme
                            |= ...
        """
        super().__init__()
        
        self.setApplicationName(app_name)
        self.setOrganizationName(kwargs.get(
            'organization', 'lib.declare_pyside'
        ))
        
        self.engine = QQmlApplicationEngine()
        self.root = self.engine.rootContext()
        self.__pyobj_holder = {}
        
        self._fine_tune()
        self._register_paths(kwargs.get('theme_dir', theme_dir))
        
        self.on_exit = super().aboutToQuit  # noqa
    
    def set_app_name(self, name: str):
        # just made a consistent snake-case function alias for external caller,
        # especially for who imports a global instance `app` from this module.
        self.setApplicationName(name)
    
    def _fine_tune(self):
        # set font 'microsoft yahei ui' if platform is windows
        from platform import system
        if system() == 'Windows':
            self.setFont('Microsoft YaHei')
    
    def _register_paths(self, theme_dir: str):
        # self.add_import_entrance(qmlside_dir)
        self.add_import_entrance(theme_dir)
    
    def add_import_entrance(self, qmldir: str):
        """
        Args:
            qmldir: The absolute path of directory, this dir should include at
                least one component library subfolder (the subfolder's first
                letter shoule be capitalized), the subfolder should include a
                file named 'qmldir' (no suffix with it).
                See examples:
                    ../qmlside/qlogger (includes 'LKQmlSide')
                    ../../theme (includes 'LightClean')
        """
        self.engine.addImportPath(qmldir)
    
    def register_pyobj(self, obj: QObject, name=''):
        """
        Register Python object to QML root context. Then we can use it as a
        global registered property across all QML files.
        
        Notes:
            This object must inherit from `PySide6.QtCore.QObject`.
            This mehod should be used before `self.start` running.
            `declare-qml` will register 'PySide' as a built-in object, please
            do not use 'PySide' for your custom object, or it may erase all
            built-in features.
            
        Args:
            obj:
            name: Object name. Suggest using capital camel case, and prefixed
                with 'Py', for example, 'PySide', 'PyHandler', 'PyHook', etc.
                If name not defined, we'll use object's class name instead.
        """
        name = name or obj.__class__.__name__
        self.root.setContextProperty(name, obj)
        self.__pyobj_holder[name] = obj
    
    def start(self, qmlfile: TPath):
        """
        Args:
            qmlfile: Pass a '.qml' file to launch the application.
                Usually the filename is 'Main.qml' or 'Homepage.qml', the name
                case is not sensitive (you can also use lower case if you like).
                Make sure the file content accords with QML syntax and the root
                item should be Window.
        
        Notice:
            It seems that `self.engine` cannot recognize abspath format, when
            we use:
                self.engine.load(<an_abspath_of_qmlfile>)
            It will raise a network error:
                QQmlApplicationengine failed to load component.
            We should add a prefix 'file:///' to it to resolve this problem.
            By the way a relative path is always safe to use.
        """
        if xpath.isabs(qmlfile): qmlfile = 'file:///' + qmlfile
        self.engine.load(qmlfile)
        self.exec()
        #   note: do not use `sys.exit(self.exec())` here, that will cause
        #   `~.py_side.pycomm.PySide` be released in advance. then qml will
        #   alert 'cannot call from null' in its destroying stage.
    
    # function alias for compatibility.
    launch = run = open = exec_ = start
    #   https://ux.stackexchange.com/questions/106001/do-we-open-or-launch-or
    #   -startapps+&cd=1&hl=zh-CN&ct=clnk&gl=sg


class Application:
    # _appcore: _Application
    
    def __init__(self, app_name='', **kwargs):
        if app_name:
            app.setApplicationName(app_name)
        if x := kwargs.get('organization'):
            app.setOrganizationName(x)
        if x := kwargs.get('theme_dir'):
            app.add_import_entrance(x)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        # from declare_foundation.context_manager import this
        # lk.logt('[D1432]', this)
        # self.start(this.represents.qmlfile)
    
    @staticmethod
    def start(qmlfile: TPath):
        app.start(qmlfile)


app = _Application()
