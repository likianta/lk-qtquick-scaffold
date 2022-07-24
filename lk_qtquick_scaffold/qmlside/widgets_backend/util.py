from os import getcwd

from .__ext__ import QObject
from .__ext__ import slot

_cwd = 'file:///' + getcwd().replace('\\', '/')


class Util(QObject):
    
    @slot(result=str)
    @slot(str, result=str)
    def get_path(self, relpath: str = '') -> str:
        if relpath == '':
            return _cwd
        else:
            return f'{_cwd}/{relpath}'
