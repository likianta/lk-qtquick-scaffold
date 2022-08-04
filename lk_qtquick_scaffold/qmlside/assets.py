from lk_utils.filesniff import normpath

from ..qt_core import QObject
from ..qt_core import slot


class Assets(QObject):
    
    def __init__(self):
        super().__init__()
        from os import getcwd
        self._cwd = 'file:///' + getcwd().replace('\\', '/')
        self._src = self._cwd
    
    def set_root(self, dir_: str):
        self._src = 'file:///' + normpath(dir_, force_abspath=True)
    
    @slot(result=str)
    @slot(str, result=str)
    def src(self, relpath: str = '') -> str:
        if relpath == '':
            return self._src
        else:
            return normpath(f'{self._src}/{relpath}')

    @slot(result=str)
    @slot(str, result=str)
    def cwd(self, relpath: str = '') -> str:
        if relpath == '':
            return self._cwd
        else:
            return normpath(f'{self._cwd}/{relpath}')


pyassets = Assets()
