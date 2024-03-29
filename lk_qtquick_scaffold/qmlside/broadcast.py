import typing as t

from ..qt_core import QObject
from ..qt_core import signal
from ..qt_core import slot


class BroadCast(QObject):
    cast = signal(str)
    
    def __init__(self):
        super().__init__()
        self._channels = {}  # type: dict[str, t.Callable]
        self.cast.connect(self._handle)
    
    @slot(str, 'any')
    def register(self, channel: str, func: t.Callable):
        self._channels[channel] = func
    
    def _handle(self, channel: str, args=None, kwargs=None):
        if channel in self._channels:
            self._channels[channel](*(args or ()), **(kwargs or {}))


pybroad = BroadCast()
