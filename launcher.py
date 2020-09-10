"""
@Author   : dingxianjie (dwx960115)
@FileName : launcher.py
@Version  : 0.1.0
@Created  : 2020-09-09
@Updated  : 2020-09-09
@Desc     :
"""
import sys

from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication
from pyhooks import PyHooks

app = QApplication()
app.setOrganizationName('Likianta')
# engine = QQmlApplicationEngine('./ui/Main.qml')
engine = QQmlApplicationEngine()
root = engine.rootContext()

_hooks = PyHooks(root)

engine.load('./qml/Main.qml')
sys.exit(app.exec_())
