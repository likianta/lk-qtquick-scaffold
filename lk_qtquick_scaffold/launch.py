"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : launch.py
@Created : 2020-08-30
@Updated : 2020-08-30
@Version : 0.1.0
@Desc    : The minimal snippet to launch application.
"""
from sys import exit
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication

app = QApplication()
engine = QQmlApplicationEngine('./qml/sample/MyWindow.qml')
exit(app.exec_())
