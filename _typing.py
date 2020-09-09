"""
@Author   : dingxianjie (dwx960115)
@FileName : _typing.py
@Version  : 0.1.0
@Created  : 2020-09-09
@Updated  : 2020-09-09
@Desc     : 
"""
from typing import *
from PySide2.QtCore import QObject
from PySide2.QtQml import QJSValue

QObj = QObject
QPath = str  # e.g. './ui/SomeFolder/SomeComp.qml'
QUid = str  # e.g. '_mouse_area'
QUrl = str  # e.g. './ui/SomeFolder/SomeComp.qml#_mouse_area'
QVal = QJSValue
# QVal = Union[str, int, float, bool, list]
QVar = 'QVariant'

# ------------------------------------------------------------------------------

QSource = QPath
