"""
@Author  : likianta <likianta@foxmail.com>
@Module  : main.py
@Created : 2020-09-20
@Updated : 2021-01-18
@Version : 0.2.9
@Desc    :
    Usage:
        from lk_qtquick_scaffold.debugger import HotReloader
        reloader = HotReloader('./my_view.qml')
        reloader.start()
"""


class HotReloader:
    loader: str
    target: str
    
    def __init__(self, target: str):
        """
        Args:
            target: see `self._locate_target`
        """
        self._locate_target(target)
    
    def _locate_target(self, target: str):
        """
        Args:
            target: A .qml file for hot loading.
        
        Notes:
            我们需要准备一个 HotReloader.qml 文件, 和一个 target (.qml) 文件.
            lk-qtquick-scaffold 会先加载 HotReloader.qml, 然后再通过
            HotReloader.qml 加载 target.
            其中, HotReloader.qml 文件由本模块所在的目录下的
            '~/LKDebugger/HotReloader.qml' 提供; target 由用户在创建类实例时传
            入.
            
            这里有一个注意事项, target 必须使用相对路径 (相对于 HotReloader
            .qml), 不能使用绝对路径. 否则会导致 target 文件中的所有 relative
            import 语句全部无法正常工作.
            当 target 与 HotReloader.qml 同盘符时, 使用 os.path.relpath 即可计算
            出此相对路径. 但是二者不同盘符时, 无法使用 os.path.relpath 计算. 我
            们的解决方法是, 复制一个 HotReloader.qml 文件到与 target 同目录下的
            '~/__lk_qtquick_scaffold__/HotReloader.qml' 路径.
            
            另外一个注意事项, os.path.relpath(p, q) 的计算是根据文件节点来的, 因
            此我们会发现, 在下面的情形中:
                |- PPP
                    |- p.qml
                |- QQQ
                    |- q.qml
               我们认为 p 相对于 q 的路径是 '../PPP/p.qml', 但 os.path 把 q.qml
               也作为一个文件节点了, 所以给出的值是 '../../PPP/p.qml', 所以我们
               用 `[3:]` 去除开头多余的 '../' 的字符.
        """
        from os.path import abspath, dirname, relpath
        
        loader = abspath(f'{dirname(__file__)}/LKDebugger/HotReloader.qml')
        target = abspath(target)
        
        if target[0] != loader[0]:
            # target 与 HotReloader.qml 不同盘, 这时我们必须将 HotReloader.qml
            # 文件放在与 target 同盘的目录下.
            # 这里我们选择放在与 target 同一目录下的 (新建一个)
            # '__lk_qtquick_scaffold__/HotReloader.qml' 路径.
            from lk_logger import lk
            lk.log('目标 qml 文件与 HotReloader.qml 位于不同盘符, 将在目标 '
                   'qml 文件同目录下创建 ~/__lk_qtquick_scaffold__/HotReloader'
                   '.qml', h='grand_parent')
            
            from os.path import exists
            if not exists(_d := abspath(
                    f'{target}/../__lk_qtquick_scaffold__')):
                from os import mkdir
                mkdir(_d)
            if not exists(_f := f'{_d}/HotReloader.qml'):
                from shutil import copyfile
                copyfile(loader, _f)
            loader = _f
        target = relpath(target, loader)[3:]
        #   [3:]: 去除开头多余的 '../' 的字符
        
        self.loader = loader
        self.target = target
    
    def start(self):
        # register hot reloader runtime functions
        from lk_qtquick_scaffold import app, pyhandler
        pyhandler.register(app.engine.clearComponentCache,
                           'clear_component_cache')
        pyhandler.register(self.get_target)
        
        # start app
        app.start(self.loader)
    
    def get_target(self):
        return self.target
