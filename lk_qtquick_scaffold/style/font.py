from .base import Base


class Font(Base):
    def _get_abbrs(self, name: str) -> (str, ...):
        if name.endswith('_m'):
            yield name[:-2]
        elif name.endswith('_default'):
            yield name[:-8]
    
    def update_from_file(self, file: str):
        from lk_utils import loads
        data: dict = loads(file)
        for k, v in data.items():
            if k == 'font_default' and v == '':
                from qtpy.QtWidgets import QApplication
                from os import name
                if name == 'nt':
                    v = 'Microsoft YaHei UI'
                else:
                    v = QApplication.font().family()  # noqa
            if isinstance(v, str) and v.startswith('$'):
                data[k] = data[v[1:]]
        self.update(**data)
