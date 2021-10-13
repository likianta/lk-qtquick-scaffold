from os import PathLike as _PathLike
from typing import *

from PySide6.QtCore import QObject as _QObject
from PySide6.QtQml import QJSValue as _QJSValue
from PySide6.QtQml import QQmlComponent as _QQmlComponent
from PySide6.QtQml import QQmlProperty as _QQmlProperty
from PySide6.QtQuick import QQuickItem as _QQuickItem
from lk_lambdex import lambdex as _lambdex

# see typical usages in `.delegators`
_TFakeModule = _lambdex('', """
    class FakeModule:
        def __getattr__(self, item):
            return None
        def __call__(self, *args, **kwargs):
            return None
    return FakeModule()
""")()

if __name__ == '__main__':
    class TQObject(_QObject, _QQuickItem):
        def get_children(self) -> list[_QObject]: pass
else:
    TQObject = _TFakeModule

# ------------------------------------------------------------------------------

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

TProperty = _QQmlProperty
TPropName: TypeAlias = str
TComponent = _QQmlComponent

TSender = tuple[TQObject, TPropName]
TReceptor = tuple[TQObject, TPropName]

TQmlFile = Union[_PathLike, str]
TComponentCache = dict[TQmlFile, TComponent]


class TJsEvaluatorCore:
    # `declare_pyside/qmlside/LKQmlSide/QmlSide.qml`
    
    @staticmethod
    def bind(t_obj: TQObject, s_obj: TQObject, expression: str): pass
    
    @staticmethod
    def connect_prop(*_, **__) -> Any: pass
    
    @staticmethod
    def create_component(_: str) -> TComponent: pass
    
    @staticmethod
    def create_object(component: TComponent, container: TQObject) -> TQObject: pass
    
    @staticmethod
    def eval_js(code: str, args: list[TQObject]): pass
    
    @staticmethod
    def test() -> str: pass
