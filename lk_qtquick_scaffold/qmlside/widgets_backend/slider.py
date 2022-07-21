from qtpy.QtCore import QObject

from ...qt_core import slot


class Slider(QObject):
    
    @slot(float, result=str)
    @slot(float, int, result=str)
    def show_value(self, value: float, precison=0) -> str:
        return f'{value * 100:.{precison}f}%'
