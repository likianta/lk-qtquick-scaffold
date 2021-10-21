from functools import wraps

from PySide6.QtCore import QObject
from PySide6.QtQml import QJSValue

from ._ext import List


def adapt_argtypes(func):
    def _adapt(obj):
        if isinstance(obj, QObject) and not hasattr(obj, 'get_children'):
            setattr(obj, 'get_children', lambda: _get_children(obj))
            return obj
        elif isinstance(obj, QJSValue):
            return obj.toVariant()
        else:
            return obj
    
    @wraps(func)
    def _wrap(*args, **kwargs):
        return func(
            *(_adapt(v) for v in args),
            **{k: _adapt(v) for k, v in kwargs.items()}
        )
    
    return _wrap


def _get_children(self: QObject) -> List[QObject]:
    """
    Notice:
        Do not use `parent.children()` directly, because there may be one
        "unknown and invalid" child object in it.
        The unknown child can be detected by querying any property of it.
        If the property values are always given `None`, that means it's a
        "unknown and invalid" child.
        Here we use `parent.children()[<some_index>].property(
        <some_property>)` to find it.
    """
    out = []
    for item in self.children():
        if item.property('enabled') is None:
            continue
        out.append(item)
        # yield item
    return out
