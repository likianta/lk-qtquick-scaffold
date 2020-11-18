"""
@Author  : likianta <likianta@foxmail.com>
@Module  : launcher.py
@Created : 2020-08-30
@Updated : 2020-11-18
@Version : 0.2.8
@Desc    :
"""
from sys import exit

from PySide2.QtCore import QObject
from PySide2.QtQml import QQmlApplicationEngine, QQmlContext
from PySide2.QtWidgets import QApplication


class Application(QApplication):
    __holder: dict  # __holder 只是为了在整个生命周期中持续持有实例, 以防止
    #   Python 垃圾回收机制误杀注入到 QML 全局变量的对象, 本身没有其他用处.
    _entrance: str
    engine: QQmlApplicationEngine
    root: QQmlContext
    
    def __init__(self, entrance: str, *lib: str, **kwargs):
        """
        :param entrance: 启动时要载入的 .qml 文件. 通常为 '{somedir}/main.qml'
            或 '{somedir}/view.qml'.
        :param lib: 要引入外部自定义 QML 模块, 则填写该模块的父目录路径. 例如,
            我们在 A 项目中引入 lk_qtquick_scaffold 脚手架项目的 LKWidget 模块,
            则:
                lib: '~/lk_qtquick_scaffold/scaffold'
        :param kwargs:
            :key 'organization'
        """
        super().__init__()
        self.setOrganizationName(kwargs.get(
            'organization', 'dev.likianta.lk_qtquick_scaffold'
        ))
        #   该步骤是为了避免在 QML 中使用 QtQuick.Dialogs.FileDialog 时, 出现警
        #   告信息:
        #       QML Settings: The following application identifiers have not
        #       been set: QVector("organizationName", "organizationDomain")
        
        self.__holder = {}
        self._entrance = entrance
        self.engine = QQmlApplicationEngine()
        self.root = self.engine.rootContext()
        
        if not lib:
            lib = (__file__.rsplit('\\', 1)[0] + '\\scaffold',)
            #   __file__ = '~\\lk_qtquick_scaffold\\lk_qtquick_scaffold\\
            #   __init__.py' -> lib = ('lk_qtquick_scaffold\\lk_qtquick_scaffold
            #   \\scaffold',)
        for p in lib:
            self.engine.addImportPath(p)
    
    def register_pyobj(self, name, handler: QObject):
        """ 将 Python 中定义好的 (继承自 QObject 的) 对象作为全局变量加载到 QML
            布局的上下文当中.
            
        1. 仅在调用 self.start() 前使用.
        2. name 建议使用大驼峰式命名, 并建议以 "Py" 开头, 例如: "PyHooks".
        3. 这些对象可以在 QML 布局中全局使用.
        """
        # 令 self.__holder 持有该实例, 避免 Python 误将 handler 引用计数归零.
        self.__holder[name] = handler
        self.root.setContextProperty(name, handler)
    
    def start(self):
        self.engine.load(self._entrance)
        exit(self.exec_())


if __name__ == '__main__':
    _app = Application('./qml/Demo/LightCleanDemo.qml', './scaffold')
    _app.start()
