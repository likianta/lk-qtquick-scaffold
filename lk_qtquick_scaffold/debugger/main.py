"""
@Author  : likianta <likianta@foxmail.com>
@Module  : main.py
@Created : 2020-09-20
@Updated : 2021-01-04
@Version : 0.2.8
@Desc    :
    Usage:
        from lk_qtquick_scaffold.debugger import HotReloader
        reloader = HotReloader('./my_view.qml')
        reloader.start()
"""
from os.path import abspath, dirname, relpath


class HotReloader:
    
    def __init__(self, target: str):
        """
        Args:
            target: A .qml file for hot loading.
        """
        self.curr_dir = dirname(__file__)
        self.loader = abspath(f'{self.curr_dir}/LKDebugger/HotReloader.qml')
        self.target = relpath(abspath(target), self.loader)[3:]
        '''           ^-----------------------------------^^--^
                                       A                    B
            A: os.path.relpath(p, q) 计算出来的是绝对路径 p 相对于绝对路径 q 的
               相对路径
            B: os.path 计算是根据文件节点来的, 因此我们会发现, 在下面的情形中:
                |- PPP
                    |- p.qml
                |- QQQ
                    |- q.qml
               我们认为 p 相对于 q 的路径是 '../PPP/p.qml', 但 os.path 把 q.qml
               也作为一个文件节点了, 所以给出的值是 '../../PPP/p.qml', 所以我们
               用 `[3:]` 去除开头多余的 '../' 的字符.
            
            另外注意: `self.target` 必须使用相对路径表示, 不能使用绝对路径.
            即:
                self.target = abspath(target)  # 错误!
                self.target = relpath(abspath(target), self.loader)[3:]  # 正确
            当采用错误的写法时, 会导致 `self.target` 所对应的 qml 文件中的
            relative import 语句全部无法正常工作.
        '''
    
    def start(self):
        # register hot reloader runtime functions
        from lk_qtquick_scaffold import app, pyhandler
        pyhandler.register_pyfunc(
            app.engine.clearComponentCache, 'clear_component_cache')
        pyhandler.register_pyfunc(self.get_target)
        
        # start app
        app.start(self.loader)
    
    def get_target(self):
        return self.target


if __name__ == '__main__':
    reloader = HotReloader(abspath('../../tests/qml/view.qml'))
    reloader.start()
