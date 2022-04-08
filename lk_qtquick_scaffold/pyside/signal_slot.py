"""
fix typehint of Signal and Slot.
"""
from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtCore import Slot


def slot(*args: type, result: Union[str, type, None] = None):
    if result is not None and result is not str and type(result) is not str:
        result = 'QVariant'
    
    def wrapper(func):
        return Slot(*args, result=result)(func)
    
    return wrapper


class SignalTypeHint:
    
    def __call__(self, *args: type):
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
