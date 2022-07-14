from qtpy.QtCore import QObject
from qtpy.QtQml import QQmlApplicationEngine
from qtpy.QtQml import QQmlContext
from qtpy.QtWidgets import QApplication


class T:
    from os import PathLike
    from typing import Union
    Path = Union[PathLike, str]


class Application(QApplication):
    engine: QQmlApplicationEngine
    root: QQmlContext
    
    # the holder is made for preventing the objects which were registered to
    #   qml side from being recycled by python garbage collector incorrectly.
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
        self.on_exit.connect(self._exit)
    
    def set_app_name(self, name: str):
        # just made a consistent snake-case function alias for external caller,
        # especially for who imports a global instance `app` from this module.
        self.setApplicationName(name)
    
    def _ui_fine_tune(self):
        from os import name
        if name == 'nt':
            self.setFont('Microsoft YaHei UI')  # noqa
    
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
    
    @staticmethod
    def register_qmltype(qobj_cls, package='LKScaffold', name: str = None):
        """
        ref: https://qmlbook.github.io/ch20-python/python.html#exposing-a-python
            -class-to-qml
        
        to use it in qml side:
            import <package> 1.0
            <class_name> { ... }
            
        example:
            # python side
            class MyObject(QObject):
                pass
            from lk_qtquick_scaffold import app
            app.register_qmltype(MyObject)
            
            # qml side
            import LKScaffold 1.0
            MyObject { ... }
        """
        from qtpy.QtQml import qmlRegisterType
        # noinspection PyTypeChecker
        qmlRegisterType(qobj_cls, package, 1, 0, name or qobj_cls.__name__)

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
    
    register = register_pyobj  # alias
    
    def start(self, qmlfile: T.Path):
        """
        Args:
            qmlfile: str filepath.
                a '.qml' file. usually it named '~/Main.qml', '~/Home.qml', etc.
                the name case is not sensitive (you can also use lower case).
        """
        from lk_utils.filesniff import normpath
        self.engine.load('file:///' + normpath(qmlfile, force_abspath=True))
        
        from os import getenv
        if getenv('QT_API') in ('pyside2', 'pyqt5'):
            self.exec_()
        else:
            self.exec()
        #   warning: do not use `sys.exit(self.exec())`, because
        #   `self.__pyobj_holder` will be released before qml triggered
        #   `Component.onDestroyed`. then there will be an error 'cannot call
        #   from null!'
    
    # alias for compatible.
    #   https://ux.stackexchange.com/questions/106001/do-we-open-or-launch-or
    #   -startapps+&cd=1&hl=zh-CN&ct=clnk&gl=sg
    launch = run = open = start
    
    def show_splash_screen(self, file: T.Path):
        from os.path import exists
        assert exists(file)
        
        from qtpy.QtCore import Qt
        from qtpy.QtGui import QPixmap
        from qtpy.QtWidgets import QSplashScreen, QWidget
        
        pixmap = QPixmap(file)  # noqa
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        splash.setMask(pixmap.mask())
        
        def on_close():
            nonlocal splash
            print(':v', 'Close splash screen')
            splash.hide()
            splash.finish(QWidget())
        
        self.engine.objectCreated.connect(on_close)  # noqa
        
        splash.show()
        self.processEvents()
    
    def _exit(self):
        """
        when user closes the app window, a weird thing happens that
        `self.engine` is not released at once.
        in the meantime, `self.__pyobj_holder` is released, which causes a
        TypeError of calling property on a null object.
        to resolve this, we need to explicitly clear `self.engine` before
        `self.__pyobj_holder`.
        
        ref:
            keywords: QML TypeError: Cannot read property of null
            link:
                https://bugreports.qt.io/browse/QTBUG-81247?focusedCommentId
                =512347&page=com.atlassian.jira.plugin.system.issuetabpanels
                :comment-tabpanel#comment-512347
        """
        print('[red dim]Exit application[/]', ':r')
        del self.engine
        self.__pyobj_holder.clear()


app = Application()
