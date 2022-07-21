from qtpy.QtCore import QObject as QObjectBase

from .signal_slot import slot


class QObject(QObjectBase):
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    @slot(name='__file__', result=str)
    def __file__(self) -> str:
        return __file__
