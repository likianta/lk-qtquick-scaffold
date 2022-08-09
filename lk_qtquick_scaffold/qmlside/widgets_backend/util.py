from .__ext__ import QObject
from .__ext__ import slot


class Util(QObject):
    
    @slot(result=str)
    def get_monospaced_font(self) -> str:
        """ get an available monospaced font family name based on OS. """
        from platform import system
        name = system()
        if name == 'Darwin':
            return 'Menlo'
        elif name == 'Windows':
            return 'Consolas'
        else:
            return 'Ubuntu Mono'
