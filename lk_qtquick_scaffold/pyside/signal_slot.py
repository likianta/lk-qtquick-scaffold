"""
fix typehint of Signal and Slot.
"""
from functools import partial
from typing import Union

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue


class DelegatedFunc:
    
    def __init__(self, func, argtypes):
        self.name = func.__name__
        self._func = func
        self._argtypes = argtypes
    
    def __get__(self, instance, owner):
        """
        issue keywords: python decorator, self, __call__, missing self
            here're references:
                1. https://stackoverflow.com/questions/57086840/decorator-class
                   -and-missing-required-positional-arguments
                2. https://stackoverflow.com/questions/5469956/python-decorator
                   -self-is-mixed-up
                3. https://stackoverflow.com/questions/57807258/passing-self
                   -parameter-during-methods-decorating-in-python/57808792
                   #57808792
        """
        return partial(self, instance)
    
    def __call__(self, *args):
        args = self._auto_convert_argtypes(args)
        return self._func(*args)
    
    def _auto_convert_argtypes(self, args: tuple):
        if len(args) > len(self._argtypes):
            self_, args = args[0], args[1:]
        else:
            self_, args = None, args
        
        new_args = []
        
        for i, a, t in zip(range(len(args)), args, self._argtypes):
            if t is QJSValue:
                new_args.append(a.toVariant())
            else:
                new_args.append(a)
        
        if self_ is None:
            return new_args
        else:
            return self_, *new_args


def slot(*argtypes: type, result: Union[str, type, None] = None):
    if result not in (None, str) and type(result) is not str:
        result = 'QVariant'
    
    new_argtypes = []
    for t in argtypes:
        if t is object:
            t = QObject
        elif t not in (bool, bytes, float, int, str, QObject):
            t = QJSValue
        new_argtypes.append(t)
    argtypes = tuple(new_argtypes)
    del new_argtypes
    
    def decorator(func):
        # print(':v', func, type(func))
        if not isinstance(func, DelegatedFunc):
            func = DelegatedFunc(func, argtypes)
        return Slot(*argtypes, name=func.name, result=result)(func)
    
    return decorator


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
