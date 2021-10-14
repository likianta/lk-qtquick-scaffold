from PySide6.QtCore import QObject
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue

strict_mode = False


# def apply_resource_manager(pkg):
#     pass


class ResourceManager(QObject):
    
    @Slot(str, result='QVariant')
    @Slot(str, QJSValue, result='QVariant')
    def get(self, name, kwargs: dict = None):
        return self._get(name, **(kwargs or {}))
    
    def _get(self, name, **kwargs):
        raise NotImplementedError
    
    def _fetch(self, name):
        assert hasattr(self, name)
        return getattr(self, name)


class BaseResourceManager(QObject):
    
    @Slot(str, result='string')
    def get(self, name):
        assert hasattr(self, name)
        return getattr(self, name)
