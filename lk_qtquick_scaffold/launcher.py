"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : launch.py
@Created : 2020-08-30
@Updated : 2020-09-14
@Version : 0.2.3
@Desc    :
"""
from sys import exit

from PySide2.QtCore import QObject
from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtWidgets import QApplication


class Application(QApplication):
    __holder: dict  # __holder 只是为了防止 Python 垃圾回收机制误杀注入到 QML 全
    #   局变量的对象
    _entrance: str
    engine: QQmlApplicationEngine
    root: QQmlContext
    
    def __init__(self, entrance: str, *lib: str, **kwargs):
        super().__init__()
        self.setOrganizationName(kwargs.get(
            'organization', 'dev.likianta.lk_qtquick_scaffold'))
        #   该步骤是为了避免在 QML 中使用 QtQuick.Dialogs.FileDialog 时, 出现警
        #   告信息:
        #       QML Settings: The following application identifiers have not
        #       been set: QVector("organizationName", "organizationDomain")'

        self._entrance = entrance
        self.__holder = {}
        self.engine = QQmlApplicationEngine()
        self.root = self.engine.rootContext()
        
        for i in lib:
            self.engine.addImportPath(i)
        
        from pyhooks import PyHooks
        self.register_pyhandler('PyHooks', PyHooks())
    
    def register_pyhandler(self, name, handler: QObject):
        """ 将 Python 中定义好的 (继承自 QObject 的) 对象作为全局变量加载到 QML
            引擎.
        1. 仅在调用 self.start() 前使用.
        2. name 建议使用大驼峰式命名, 并建议以 "Py" 开头, 例如: "PyHooks".
        3. 这些对象可以在 QML 布局中全局使用.
        """
        self.__holder[name] = handler
        self.root.setContextProperty(name, handler)
    
    def start(self):
        self.engine.load(self._entrance)
        exit(self.exec_())


if __name__ == '__main__':
    _app = Application('./qml/Demo/LightCleanDemo.qml',
                       './qml')
    _app.start()
