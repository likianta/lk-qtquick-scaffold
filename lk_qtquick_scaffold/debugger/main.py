"""
@Author  : likianta <likianta@foxmail.com>
@Module  : main.py
@Created : 2020-09-20
@Updated : 2020-11-29
@Version : 0.2.3
@Desc    :
    Usage:
        from lk_qtquick_scaffold.debugger import HotReloader
        reloader = HotReloader('./my_view.qml')
        reloader.launch()
"""
from os.path import abspath, dirname


class HotReloader:
    
    def __init__(self, target: str):
        """
        Args:
            target: A .qml file for hot loading.
        """
        self.curr_dir = dirname(__file__)
        self.viewer = abspath(f'{self.curr_dir}/HotReloader.qml')
        self.target = abspath(target)
        
        from platform import system
        if system() == 'Windows':
            self.target = 'file:///' + self.target
            
    def launch(self):
        from lk_qtquick_scaffold import app, pyhandler
        pyhandler.register_pyfunc(app.engine.clearComponentCache,
                                  'clear_component_cache')
        pyhandler.register_pyfunc(self.get_target)
        app.start(self.viewer)
        
    def get_target(self):
        return self.target


if __name__ == '__main__':
    reloader = HotReloader(abspath('../../tests/qml/view.qml'))
    reloader.launch()
