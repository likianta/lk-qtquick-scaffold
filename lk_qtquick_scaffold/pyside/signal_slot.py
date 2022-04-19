"""
fix typehint of Signal and Slot.
"""
from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue

# hold some objects globally (elevate their refcount), to prevent python gc.
__global_life_cycle = []


def slot(*argtypes: type, name='', result: Union[str, type, None] = None):
    if result not in (None, str) and type(result) is not str:
        result = 'QVariant'
    
    argtypes = _reformat_argtypes(argtypes)
    
    def decorator(func):
        nonlocal argtypes, name, result
        __global_life_cycle.append(
            Slot(*argtypes, name=(name or func.__name__), result=result)(func)
        )
        return func
    
    return decorator


def _reformat_argtypes(argtypes: tuple) -> tuple:
    new_argtypes = []
    for t in argtypes:
        if t is object:
            t = QObject
        elif t not in (bool, bytes, float, int, str, QObject):
            t = QJSValue
        new_argtypes.append(t)
    return tuple(new_argtypes)


# -----------------------------------------------------------------------------

class SignalTypeHint:
    
    def __call__(self, *argtypes: type):
        pass
    
    def connect(self, func):
        pass
    
    def emit(self, *args):
        pass


signal: SignalTypeHint


def __init__():
    global signal
    signal = Signal


__init__()
