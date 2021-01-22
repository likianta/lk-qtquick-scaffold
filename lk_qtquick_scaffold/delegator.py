from PySide2.QtCore import QObject


class QObjectDelegator(QObject):
    
    def __init__(self, instance, registered_methods):
        super().__init__()
        self.delegate = instance
        
        for method_name, (name, narg) in registered_methods:
            #   the `name` equals to `method_name`, or an alias of `method_name`
            method = getattr(self.delegate, method_name)
            self._register(method, name, narg)
            pass
