"""
@Author   : likianta <likianta@foxmail.com>
@FileName : _typing.py
@Version  : 0.2.0
@Created  : 2020-09-09
@Updated  : 2020-11-26
@Desc     : 
"""
from typing import *
from PySide2.QtCore import QObject as _QObject
from PySide2.QtQml import QJSValue as _QJSValue


class QType:
    QPath = str  # e.g. './ui/SomeFolder/SomeComp.qml'
    QSource = QPath
    
    QUid = str  # e.g. '_mouse_area'
    QUrl = str  # e.g. './ui/SomeFolder/SomeComp.qml#_mouse_area'
    QObj = _QObject
    
    QVar = 'QVariant'
    QVal = _QJSValue
    PyVal = Union[bool, float, int, str, list, dict]


class HooksType:
    Datapot = Dict[str, Tuple[QType.QVal, QType.QSource]]
    Hooks = Set[QType.QObj]
    Holder = Dict[QType.QPath, Dict[QType.QUid, QType.QObj]]
    GetRet = Union[QType.QObj,
                   List[QType.QObj],
                   Dict[QType.QUid, QType.QObj],
                   None]
    UnknownGet = Union[QType.QUrl, QType.QPath, QType.QVal]
    UnknownArg1 = Union[QType.QPath, QType.QUrl, QType.QVal]
    UnknownArg2 = Union[QType.QObj, QType.QVal]


class PyHandlerType:
    Func = Callable
    FuncName = str
