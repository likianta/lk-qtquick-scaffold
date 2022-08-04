from lk_utils.filesniff import normpath

from ..qt_core import QObject
from ..qt_core import slot


class Assets(QObject):
    
    def __init__(self):
        super().__init__()
        from os import getcwd
        self._root = 'file:///' + getcwd().replace('\\', '/')
    
    def set_root(self, dir_: str):
        self._root = 'file:///' + normpath(dir_, force_abspath=True)
    
    @slot(result=str)
    @slot(str, result=str)
    def get(self, relpath: str = '') -> str:
        if relpath == '':
            return self._root
        else:
            return normpath(f'{self._root}/{relpath}')


pyassets = Assets()
