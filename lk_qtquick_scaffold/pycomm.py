"""
@Author   : likianta (likianta@foxmail.com)
@FileName : pycomm.py
@Version  : 0.7.0
@Created  : 2020-09-09
@Updated  : 2020-11-29
@Desc     : 
"""
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
    __pyfunc_dict = {}
    
    def __init__(self, object_name=''):
        super().__init__()
        from . import app
        self.object_name = object_name or self.__class__.__name__
        app.register_pyobj(self, self.object_name)
    
    def register_pyfunc(self, func: PyHandlerType.Func, name=''):
        """
        References:
            https://medium.com/%40mgarod/dynamically-add-a-method-to-a-class-in\
            -python-c49204b85bd6+&cd=3&hl=zh-CN&ct=clnk&gl=sg
        """
        name = name or func.__name__
        # lk.loga(name, h='parent')
        self.__pyfunc_dict[name] = func
    
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
        return self.main(func_name, param)
    
    def main(self, method: str, param):
        lk.loga(method, param)
        try:
            if param is None:
                return self.__pyfunc_dict[method]()
            else:
                return self.__pyfunc_dict[method](param)
        except KeyError:
            raise Exception('Method is not registered!', method, param)


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
        self._holder = {}
        self.__inited = True
        #   注意, 双下划线开头的 '__inited' 会被特殊处理. 它在 self.__dict__ 中
        #   以 '_QObjectWrapper__inited' 显示, 而非 '__inited'.
    
    def children(self):
        """
        Notes:
            在 QML 中调用 item.children 和在 Python 中调用 item.children() 返回的结果
            是不同的! 前者返回的是正常的 children 列表, 后者返回的列表中会多出一个未知的
            child (暂不清楚原因), 而且该 child 的位置是任意的. 该 child 的特征是: 它的所
            有属性的值都是 None (正常的 child 的属性值可以是 str, bool, etc. 但不会是
            None), 凭此特征来识别并从 Python children 列表中剔除它.
        """
        out = []
        for child in self.children():
            if child.property('enabled') is not None:
                out.append(QObjectDelegator(child))
        assert len(out) == len(self.children()) - 1
        return out  # type: List[QObjectDelegator]
    
    def __getattr__(self, item):
        """
        References:
            https://stackoverflow.com/questions/54695976/how-can-i-update-a-qml
            -objects-property-from-my-python-file
        """
        if '_QObjectWrapper__inited' not in self.__dict__:
            raise Exception('QObjectWrapper is not fully initialized!')
        prop = QQmlProperty(self.qobj, item)
        if isinstance((out := prop.read()), QType.QObj):
            out = QObjectDelegator(out)
        else:
            self._holder[item] = out
        return out
    
    def __setattr__(self, key, value):
        if '_QObjectWrapper__inited' not in self.__dict__:
            self.__dict__[key] = value
            return
        if (x := self._holder.get(key)) is not None:
            #   这个步骤是为了改善赋值的, 如果前后的值没有变化, 则不更新
            #   QObject. (PS: 其实作用不是很大, 未来会移除此判断)
            self._holder.pop(key)
            if value == x:
                return  # no modified, do nothing
        prop = QQmlProperty(self.qobj, key)
        prop.write(value)
