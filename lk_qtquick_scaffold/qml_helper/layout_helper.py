"""
@Author   : likianta <likianta@foxmail.com>
@FileName : layout_helper.py
@Version  : 0.2.0
@Created  : 2020-11-12
@Updated  : 2020-11-12
@Desc     : 
"""
from functools import wraps

from PySide2.QtQml import QQmlProperty

from _typing import *


class QObjectWrapper:
    
    def __init__(self, qobj):
        self.qobj = qobj
        self._holder = {}
        self.__inited = True
        #   注意, 双下划线开头的 '__inited' 会被特殊处理. 它在 self.__dict__ 中
        #   以 '_QObjectWrapper__inited' 显示, 而非 '__inited'.
    
    def children(self):
        out = []
        for child in self.children():
            if child.property('enabled') is not None:
                out.append(QObjectWrapper(child))
        return out  # type: List[QObjectWrapper]
    
    def __getattr__(self, item):
        """
        REF: https://stackoverflow.com/questions/54695976/how-can-i-update-a-qml
             -objects-property-from-my-python-file
        """
        if '_QObjectWrapper__inited' not in self.__dict__:
            raise Exception('QObjectWrapper is not fully initialized!')
        prop = QQmlProperty(self.qobj, item)
        if isinstance((out := prop.read()), QObj):
            out = QObjectWrapper(out)
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


def adapt_types(func):
    """ 将从 QML 传过来的参数进行转换后再交给主体函数
    https://www.runoob.com/w3cnote/python-func-decorators.html
    """
    
    @wraps(func)
    def decorated(*args, **kwargs):
        new_args = []
        for i in args:
            if isinstance(i, QObj):
                new_args.append(QObjectWrapper(i))
            elif isinstance(i, QVal):
                new_args.append(i.toVariant())
            else:
                new_args.append(i)
        return func(*new_args, **kwargs)
    
    return decorated


@adapt_types
def set_children_props(parent: QObjectWrapper, props: dict):
    for child in parent.children():
        for p, v in props.items():
            if p == 'size':
                if isinstance(v, str):
                    assert v in ('ifill', 'fill', 'ofill',
                                 'iwrap', 'wrap', 'owrap')
                    w, h = parent.width, parent.height
                    
                    if v == 'ifill':
                        # 注: padding, leftPadding, rightPadding 是不相关的.
                        # 比如, padding 是 10.0 但 leftPadding 和 rightPadding
                        # 可能是 None.
                        p = parent.padding or 0
                        
                        lp = parent.leftPadding or p
                        rp = parent.rightPadding or p
                        child.width = w - lp - rp
                        
                        tp = parent.topPadding or p
                        bp = parent.bottomPadding or p
                        child.height = h - tp - bp
                    
                    elif v == 'fill':
                        child.width = w
                        child.height = h
                    
                    elif v == 'ofill':
                        m = parent.anchors.margins or 0
                        
                        lm = parent.anchors.leftMargins or m
                        rm = parent.anchors.rightMargins or m
                        child.width = w + lm + rm
                        
                        tm = parent.anchors.topMargins or m
                        bm = parent.anchors.bottomMargins or m
                        child.height = h + tm + bm
                    
                    else:
                        raise Exception('Wrap is not support for now!')
                elif isinstance(v, (tuple, list)):
                    # assert len(v) == 2
                    w, h = v
                    child.width = w
                    child.height = h
            elif p == 'pos':
                pass
