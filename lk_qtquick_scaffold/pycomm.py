"""
@Author   : likianta (likianta@foxmail.com)
@FileName : pycomm.py
@Version  : 0.7.2
@Created  : 2020-09-09
@Updated  : 2020-12-04
@Desc     : 
"""
from collections import defaultdict
from functools import wraps

from PySide2.QtCore import Slot
from PySide2.QtQml import QQmlProperty
from lk_logger import lk

from ._typing import *


class PyHandler(QType.QObj):
    """ Python Communication with Qml Runtime.

    Usages:
        See 'docs/PyComm 使用示例.md'
    """
    __pyfunc_holder = {}
    __pyclass_holder = defaultdict(lambda: defaultdict())
    
    def __init__(self, object_name=''):
        super().__init__()
        from . import app
        self.object_name = object_name or self.__class__.__name__
        app.register_pyobj(self, self.object_name)
    
    # --------------------------------------------------------------------------
    
    def register(self, name='', instance: bool = False):
        """ Decorator of register, made for easily registering functions to
            PyHandler.
        
        Args:
            name: function's name, usually just leave it blank so PyHandler uses
                `function.__name__` as its name, otherwise you can pass in a
                custom name as an alias, it likes:
                    from lk_qtquick_scaffold import pyhandler
                    @pyhandler(name='doSomthingLater')
                               ^--------------------^
                               # If you like using camelCase laterly in Qml.
                    def do_something_later():
                        pass
            instance (bool): When you decorate a instance's method, pass it True.
                Examples:
                    from lk_qtquick_scaffold import pyhandler
                    class AAA:
                        @pyhandler.register(instance=True)
                                            ^-----------^
                        def aaa(self, n=10):
                                ^--^
                                # (1/2) Notice there is a `self`, we should
                                # pass `instance=True` to decorator.
                            print(self.m + n)
                            
                        def __init__(self):
                            self.m = 12
                            pyhandler.register_pyinst(self)
                            # (2/2) And we must register the 'self' instance to
                            # pyhandler once the instance is initialized.
        
        Examples:
            from lk_qtquick_scaffold import pyhandler
            
            @pyhandler.register()
            def bbb():
                pass
            
            class AAA:
                def __init__(self):
                    pyhandler.register_pyinst(self)
                @pyhandler.register(instance=True)
                def aaa(self):
                    pass
        """
        
        def decor0(func):
            if instance:
                self.register_pyclass(func, name)
            else:
                self.register_pyfunc(func, name)
            
            @wraps(func)
            def decor1(*args, **kwargs):
                return func(*args, **kwargs)
            
            return decor1
        
        return decor0
    
    def register_pyfunc(self, func: PyHandlerType.Func, name=''):
        """ Register Python functions.
        
        References:
            https://medium.com/%40mgarod/dynamically-add-a-method-to-a-class-in\
            -python-c49204b85bd6+&cd=3&hl=zh-CN&ct=clnk&gl=sg
        """
        name = name or func.__name__
        lk.loga('Register function', name, h='parent')
        self.__pyfunc_holder[name] = func

    # noinspection PyUnresolvedReferences
    def register_pyclass(self, method: PyHandlerType.Method, name=''):
        """ Register Python class methods. """
        class_name = method.__class__.__name__
        method_name = method.__name__
        self.__pyclass_holder[class_name][method_name] = name or method_name
    
    def register_pyinst(self, instance):
        """ Register instance. """
        class_name = instance.__class__.__name__
        for method_name, method_alias in \
                self.__pyclass_holder[class_name].items():
            method = getattr(instance, method_name)
            self.register_pyfunc(method, method_alias)
    
    # --------------------------------------------------------------------------
    
    @Slot(PyHandlerType.FuncName, result=QType.QVar)
    @Slot(PyHandlerType.FuncName, QType.QVal, result=QType.QVar)
    def call(self, func_name: PyHandlerType.FuncName, param: QType.QVal = None):
        """ Call Python functions in Qml.
        
        Args:
            func_name
            param
        
        Examples:
            // view.qml
            Item {
                property string directory
                Component.onCompleted: {
                    const files = PyHandler.call('get_files', this.directory)
                }
            }
        """
        if param is not None:
            param = param.toVariant()
        try:
            if param is None:
                return self.__pyfunc_holder[func_name]()
            else:
                return self.__pyfunc_holder[func_name](param)
        except KeyError:
            raise Exception('Method is not registered!', func_name, param)


# ------------------------------------------------------------------------------
# Adaptor

def adapt_type(func):
    """ 将从 QML 传过来的参数进行类型适配后再交给目标函数.

    References:
        Decorator: https://www.runoob.com/w3cnote/python-func-decorators.html

    Examples:
        def foo(qitem, qlist, qstr):
            print(type(qitem))  # -> QObject (QType.QObj)
            print(type(qlist))  # -> QJSValue (QType.QVal)
            print(type(qstr))   # -> Py str

        @adapt_type
        def bar(qitem, qlist, qstr):
            print(type(qitem))  # -> QObjectDelegator
            print(type(qlist))  # -> Py list
            print(type(qstr))   # -> Py str
    """
    
    @wraps(func)
    def decor(*args, **kwargs):
        new_args = []
        for i in args:
            if isinstance(i, QType.QObj):
                new_args.append(QObjectDelegator(i))
            elif isinstance(i, QType.QVal):
                new_args.append(i.toVariant())
            else:
                new_args.append(i)
        return func(*new_args, **kwargs)
    
    return decor


class QObjectDelegator:
    
    def __init__(self, qobj):
        self.qobj = qobj
        self.__inited = True
        #   注意, 双下划线开头的 '__inited' 会被特殊处理. 它在 self.__dict__ 中
        #   以 '_QObjectWrapper__inited' 显示, 而非 '__inited'.
    
    def children(self):
        """
        Notes:
            在 QML 中调用 item.children 和在 Python 中调用 item.children() 返回
            的结果可能是不同的! 前者返回的是正常的 children 列表, 后者返回的列表
            中有时候会多出一个未知的 child (暂不清楚原因), 而且该 child 的位置是
            任意的.
            该 child 的特征是: 它的所有属性的值都是 None (正常的 child 的属性值
            可以是 str, bool, etc. 但不会是 None), 凭此特征来识别并从 Python
            children 列表中剔除它.
        """
        out = []
        for child in self.qobj.children():
            if child.property('enabled') is not None:
                out.append(QObjectDelegator(child))
        assert len(self.qobj.children()) - len(out) <= 1
        return out  # type: List[QObjectDelegator]
    
    def __getattr__(self, item):
        """
        Examples:
            # assume `a` is a Rectangle QObject
            b = QObjectDelegator(a)
            print(b.width)
            print(b.border.width)
        
        References:
            https://stackoverflow.com/questions/54695976/how-can-i-update-a-qml
            -objects-property-from-my-python-file
        """
        if '_QObjectDelegator__inited' not in self.__dict__:
            raise Exception('QObjectDelegator is not fully initialized!')
        prop = QQmlProperty(self.qobj, item)
        data = prop.read()
        if isinstance(data, QType.QObj):
            return QObjectDelegator(data)
        else:
            return data
    
    def __setattr__(self, key, value):
        """
        Examples:
            # assume `a` is a Rectangle QObject
            b = QObjectDelegator(a)
            b.width = 100
            b.border.width = 2
        """
        if '_QObjectDelegator__inited' not in self.__dict__:
            self.__dict__[key] = value
            return
        prop = QQmlProperty(self.qobj, key)
        prop.write(value)
    
    def __getitem__(self, item):
        """
        Examples:
            # assume `a` is a Rectangle QObject
            b = QObjectDelegator(a)
            print(b['width'])
            print(b['border']['width'])
        """
        prop = QQmlProperty(self.qobj, item)
        data = prop.read()
        if isinstance(data, QType.QObj):
            return QObjectDelegator(data)
        else:
            return data
    
    def __setitem__(self, key, value):
        """
        Examples:
            # assume `a` is a Rectangle QObject
            b = QObjectDelegator(a)
            b['width'] = 100
            b['border']['width'] = 2
        """
        prop = QQmlProperty(self.qobj, key)
        prop.write(value)
