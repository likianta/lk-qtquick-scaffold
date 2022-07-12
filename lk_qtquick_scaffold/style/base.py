from qtpy.QtQml import QQmlPropertyMap


class Base(QQmlPropertyMap):
    
    def __init__(self):
        super().__init__()
    
    def update(self, **kwargs):
        # https://stackoverflow.com/questions/62629628/attaching-qt-property-to
        # -python-class-after-definition-not-accessible-from-qml
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.insert(k, v)
            for k_abbr in self._get_abbrs(k):
                self.insert(k_abbr, v)
    
    def update_from_file(self, file: str):
        from lk_utils import loads
        data: dict = loads(file)
        for k, v in data.items():
            if isinstance(v, str) and v.startswith('$'):
                data[k] = data[v[1:]]
        self.update(**data)
    
    def _get_abbrs(self, name: str) -> (str, ...):
        raise NotImplementedError
