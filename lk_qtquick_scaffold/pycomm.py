"""
@Author   : likianta (likianta@foxmail.com)
@FileName : pycomm.py
@Version  : 0.8.0
@Created  : 2020-09-09
@Updated  : 2021-01-20
@Desc     : 
"""
from collections import defaultdict
from functools import wraps

from PySide2.QtCore import Slot
from PySide2.QtQml import QQmlProperty
from lk_logger import lk

from ._typing import *


class PyRegister:
    _pyclass_holder = defaultdict(lambda: defaultdict())
    _pyfunc_holder = {}
    
    #   {func_name: {func, narg}, ...}
    #       func_name: str. function's name
    #       func: function (or instantiated method)
    #       narg: 'number of arguments', aka arguments count, int.
    #           see `PyHandler.call`
    
    def signup(self, name='', arg0=''):
        """ Sign up

        Args:
            name:
            arg0: ''|'self'|'cls'. 如果方法的第一个参数是 'self' 或 'cls', 请传
                入 'self'|'cls'. 例如:
                    class AAA:
                        @pyreg.signup(arg0='self')
                        def mmm(self):
                            pass

        Notes:
            1. 如果目标方法同时被 staticmethod 装饰, 您需要先写 `@staticmethod`:
                class AAA:
                    @pyreg.signup
                    @staticmethod
                    def mmm():
                        pass
            2. 您不可以用本方法装饰 class. 例如, 下面的做法是错误的:
                @pyreg.signup  # wrong
                class AAA:
                    pass
            3. 实例函数必须为参数 arg0 传入 'self', 否则将出现脱离预期的行为.
                class AAA:
                    @pyreg.signup(arg0='self')
                    #             ^---------^
                    def mmm(self):
                    #       ^--^
                        pass
        """
        
        def wrap0(func):
            nonlocal name, arg0
            
            name = name or func.__name__
            narg = func.__code__.co_nlocals
            if arg0: narg -= 1
            
            if arg0 == '':
                self._register(func, name, narg)
            elif arg0 == 'self':
                self._register_method(func, name, narg)
            elif arg0 == 'cls':
                raise Exception('暂不支持注册类对象!')
            
            @wraps(func)
            def wrap1(*args, **kwargs):
                return func(*args, **kwargs)
            
            return wrap1
        
        return wrap0
    
    def _register(self, func, name: str, narg: int):
        self._pyfunc_holder[name] = (func, narg)
    
    def _register_class(self, cls, name):
        self._pyclass_holder[name] = cls
    
    def _register_function(self, func, name, narg):
        self._register(name, func, narg)
    
    def _register_instance(self, inst):
        class_name = inst.__class__.__name__
        for method_name, (name, narg) in \
                self._pyclass_holder[class_name].items():
            #   the `name` equals to `method_name`, or an alias of `method_name`
            method = getattr(inst, method_name)
            self._register(method, name, narg)
    
    register_instance = _register_instance
    
    def _register_method(self, method, name, narg):
        class_name = method.__qualname__.split('.')[-2]
        ''' e.g.
            class AAA:
                def mmm(self):
                    pass
                    
                class BBB:
                    def nnn(self):
                        pass
            
            print(AAA.mmm.__qualname__)  # -> 'AAA.mmm'
            print(BBB.nnn.__qualname__)  # -> 'AAA.BBB.nnn'
            
            don't use `class_name = method.__class__.__name__`, its value is
            always 'function'.
        '''
        method_name = method.__name__
        lk.loga(class_name, method_name)
        self._pyclass_holder[class_name][method_name] = (name, narg)
    
    def register(self, func, name=''):
        """ 注册.

        References:
            https://medium.com/%40mgarod/dynamically-add-a-method-to-a-class-in\
            -python-c49204b85bd6+&cd=3&hl=zh-CN&ct=clnk&gl=sg
            https://blog.csdn.net/Wu_Victor/article/details/84334814

        关于 "登记" (PyRegister.signup) 和 "注册" (PyRegister.register) 的区别:
            注: 该解释仅为了便于记忆和使用, 而非公式或通用的准则.
            "登记" 的主语是 "人", 这里我们把要登记的 function 或 method 作为
            "人", 因此它被用于装饰器的写法:
                @pyregister.signup
                def myfunc():  # 'myfunc' signs itself up to 'pyregister'
                    pass
            "注册" 的主体是 "注册处", 这里我们把 PyRegister 作为 "注册处", 因此
            它被提供于集中的场所进行集体的注册活动:
                def register_all_methods(*methods):
                    for m in methods:
                        pyregister.register(m)
                        # 'pyregister' registers 'm' to its roster
        """
        name = name or func.__name__
        # lk.loga(type(func).__name__, h='parent')
        if (t := type(func).__name__) in ('function', 'method'):
            narg = func.__code__.co_nlocals
            if t == 'method': narg -= 1
            self._register(func, name, narg)
        elif t == 'builtin_function_or_method':
            self._register(func, name, -1)
        else:
            self._register_instance(func)
        return name


class PyHandler(QType.QObj, PyRegister):
    """ Python Communication with Qml Runtime.

    Usages:
        See 'docs/PyComm 使用示例.md'
    """
    
    def __init__(self, object_name=''):
        super().__init__()
        from . import app
        self.object_name = object_name or self.__class__.__name__
        app.register_pyobj(self, self.object_name)
    
    @Slot(PyHandlerType.FuncName, result=QType.QVar)
    @Slot(PyHandlerType.FuncName, QType.QVal, result=QType.QVar)
    @Slot(PyHandlerType.FuncName, QType.QVal, QType.QVal, result=QType.QVar)
    def call(self, func_name, args=None, kwargs=None):
        """ Call Python functions in Qml.
        
        在 Qml 端, 支持以下三种形式的传参:
            PyHandler.call(func_name)
                func_name: 类型是 string, 指的是在 Python 端已注册到 PyHandler
                    ._pyfunc_holder 的函数的名字
            PyHandler.call(func_name, args)
                args: 当表示单参数时, 类型可以是 null, boolean, string, int,
                    real, Array, Object, QObject; 当表示多参数时, 只能是 Array.
                    注意: 这里单参数表示为 Array 时可能与多参数的类型混淆,
                    PyHandler 会自动区分
            PyHandler.call(func_name, args, kwargs)
                kwargs: 类型必须是 Object
                    注意: kwargs 仅做有限程度的支持! 当您传入 kwargs 时, args 必
                        须是多参数形式 (即必须是 Array)
        注: 一个更简单的理解是, Qml 端调用 PyHandler.call 的标准形式是:
            PyHandler.call(func_name, [...], {k: v, ...})
                                      ^---^
            本方法的优化点在于, 它可以自动判断 `[...]` 究竟是指 "一个值类型为列
            表的参数", 还是 "多个参数的值组成的列表".
        
        注意事项:
            1. 假设有注册函数:
                def aaa(x, *args):
                    pass
               Qml 端调用 `PyHandler.call('aaa', [1, 2, 3])`, 则认为 `x = 1`,
               `args = (2, 3)`;
               Qml 端调用 `PyHandler.call('aaa', [[1, 2, 3]])`, 则认为
               `x = [1, 2, 3]`, `args = ()`
        
        Args:
            func_name (PyHandlerType.FuncName):
            args (QType.QVal):
            kwargs (QType.QVal):
        
        Examples:
            # control.py
            # 假设这些是注册到 pyhandler 的函数
            def test1():
                print('this is test1')
            def test2(x):
                print(x)
            def test3(x, y):
                print(x, y)
            def test4(x, y, z=0):
                print(x, y, z)
            
            // view.qml
            Item {
                Component.onCompleted: {
                    PyHandler.call('test1')  # -> 控制台打印 'this is test1'
                    PyHandler.call('test2', 12)  #  -> 控制台打印 '12'
                    PyHandler.call('test3', [12, 14])  #  -> 控制台打印 '12 14'
                    PyHandler.call('test4', [12, 14], {z: 1})  #  -> 控制台打印
                    #   '12 14 1'
                    
                    # 对于 test4, 您还可以这样做:
                    PyHandler.call('test4', [12, 14, 1])
                    PyHandler.call('test4', [], {x: 12, y: 14, z: 1})
                    PyHandler.call('test4', [12], {y: 14, z: 1})
                }
            }
        """
        func, narg = self._pyfunc_holder[func_name]  # narg: 'number of args'
        
        args = [] if args is None else (args.toVariant() or [])
        kwargs = {} if kwargs is None else (kwargs.toVariant() or {})
        
        if kwargs:
            return func(*args, **kwargs)
        elif narg == 0:
            return func()
        elif narg == -1:
            return func(*args)
        else:
            if isinstance(args, list):
                if narg > 1:
                    return func(*args)
            # this is a feature
            return func(args)


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
