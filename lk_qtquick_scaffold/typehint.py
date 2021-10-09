from os import PathLike as _PathLike
from typing import *

from PySide6.QtQml import QJSValue as _QJSValue

TPath = Union[_PathLike, str]

TArg0 = Literal['', 'self', 'cls']
TNArgs = int  # nargs: 'number of args', int == -1 or >= 0. -1 means uncertain.

TPyClassName = str
TPyFuncName = str
TPyMethName = str
_TRegisteredName = str  # usually this name is same with `TPyFuncName` or
#   `TPyMethName`, but you can define it with a custom name (something likes
#   alias).

TPyClassHolder = dict[
    TPyClassName, dict[
        TPyMethName, tuple[_TRegisteredName, TNArgs]
    ]
]

_TPyFunction = Callable
TPyFuncHolder = dict[_TRegisteredName, tuple[_TPyFunction, TNArgs]]

TQVar = 'QVariant'
TQVal = _QJSValue
