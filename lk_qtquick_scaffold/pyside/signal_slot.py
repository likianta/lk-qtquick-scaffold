"""
fix typehint of Signal and Slot.
"""
from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue


def slot(*argtypes: type, result: Union[str, type, None] = None):
    if result is not None and result is not str and type(result) is not str:
        result = 'QVariant'
    
    new_argtypes = []
    for t in argtypes:
        if t not in (bool, float, int, str):
            t = QJSValue
        new_argtypes.append(t)
    argtypes = tuple(new_argtypes)
    del new_argtypes
    
    def _auto_convert_argtypes(*args):
        nonlocal argtypes
        
        if len(args) > len(argtypes):
            self, args = args[0], args[1:]
        else:
            self, args = None, args
            
        new_args = []
        
        for i, a, t in zip(range(len(args)), args, argtypes):
            if t is QJSValue:
                new_args.append(a.toVariant())
            else:
                new_args.append(a)
        
        if self is None:
            return new_args
        else:
            return self, *new_args
    
    def wrapper(func):
        delegate_func = lambda *args: func(*_auto_convert_argtypes(*args))
        return Slot(*argtypes, name=func.__name__, result=result)(delegate_func)
    
    return wrapper


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
