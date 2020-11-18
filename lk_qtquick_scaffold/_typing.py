"""
@Author   : likianta <likianta@foxmail.com>
@FileName : _typing.py
@Version  : 0.1.0
@Created  : 2020-09-09
@Updated  : 2020-11-18
@Desc     : 
"""
from typing import *
from PySide2.QtCore import QObject as _QObject
from PySide2.QtQml import QJSValue as _QJSValue

QPath = str  # e.g. './ui/SomeFolder/SomeComp.qml'
QSource = QPath

QUid = str  # e.g. '_mouse_area'
QUrl = str  # e.g. './ui/SomeFolder/SomeComp.qml#_mouse_area'
QObj = _QObject

QVar = 'QVariant'
QVal = _QJSValue
# QVal = Union[str, int, float, bool, list]
PyVal = Union[bool, float, int, str, list, dict]
