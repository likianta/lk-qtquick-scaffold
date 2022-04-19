from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import QQmlContext
from PySide6.QtWidgets import QApplication


class T:
    from os import PathLike
    from typing import Union
    Path = Union[PathLike, str]


class Application(QApplication):
    engine: QQmlApplicationEngine
    root: QQmlContext
    
    # the holder is made for preventing the objects which were registered to
    # qml side from being recycled by python garbage collector incorrectly.
    __pyobj_holder: dict[int, QObject]
    
    def __init__(self, app_name='LK QtQuick Scaffold App', **kwargs):
        """
        Args:
            app_name: str
                set application name.
                the name can laterly be changed by calling `self.set_app_name`.
            kwargs:
                organization: str[default='dev.likianta.lk_qtquick_scaffold']
                    set an organization name, this avoids an error from
                    `QtQuick.Dialogs.FileDialog`.
                    note: what did the error look like?
                        QML Settings: The following application identifiers
                        have not been set: QVector("organizationName",
                        "organizationDomain")
        """
        from lk_utils import relpath
        
        super().__init__()
        
        self.setApplicationName(app_name)
        self.setOrganizationName(kwargs.get(
            'organization', 'dev.likianta.lk_qtquick_scaffold'
        ))
        
        self.engine = QQmlApplicationEngine()
        self.root = self.engine.rootContext()
        self.__pyobj_holder = {}
        
        self._ui_fine_tune()
        self.register_qmldir(relpath('../widgets_lib'))
        self.register_qmldir(relpath('../themes'))
        
        self.on_exit = super().aboutToQuit  # noqa
    
    def set_app_name(self, name: str):
        # just made a consistent snake-case function alias for external caller,
        # especially for who imports a global instance `app` from this module.
        self.setApplicationName(name)
    
    def _ui_fine_tune(self):
        from platform import system
        if system() == 'Windows':
            self.setFont('Microsoft YaHei UI')
    
    def register_qmldir(self, qmldir: str):
        """
        Args:
            qmldir: str dirpath
                this directory should include at least one sub folder, which is
                available for qml to import.
                the sub folders should contain one 'qmldir' file, and multiple
                '*.qml' files. see example of '../widgets_lib'.
        """
        self.engine.addImportPath(qmldir)
    
    def register_pyobj(self, instance: QObject, name=''):
        """
        register a QObject based instance to qml global namespace (i.e. qml's
        root context).
        
        Args:
            instance:
            name:
                what it named in qml.
                if not given, will use object's class name.
                suggest to be pascal case, and prefix with 'Py'. for example,
                'PyHandler', 'PyImageProvider', 'PyDataTrainer', etc.
        
        Warning:
            use this method before calling `self.start`.
        """
        name = name or instance.__class__.__name__
        self.root.setContextProperty(name, instance)
        self.__pyobj_holder[id(instance)] = instance
    
    def start(self, qmlfile: T.Path):
        """
        Args:
            qmlfile: str filepath.
                a '.qml' file. usually it named '~/Main.qml', '~/Home.qml', etc.
                the name case is not sensitive (you can also use lower case).
        """
        from PySide6.QtCore import QUrl
        # if xpath.isabs(qmlfile): qmlfile = 'file:///' + qmlfile
        self.engine.load(QUrl(qmlfile))
        self.exec()
        #   warning: do not use `sys.exit(self.exec())`, because
        #   `self.__pyobj_holder : values` will be released before qml
        #   triggered `Component.onDestroyed`. then there will be an error
        #   'cannot call from null!'
    
    # alias for compatible.
    launch = run = open = start
    #   https://ux.stackexchange.com/questions/106001/do-we-open-or-launch-or
    #   -startapps+&cd=1&hl=zh-CN&ct=clnk&gl=sg


app = Application()
