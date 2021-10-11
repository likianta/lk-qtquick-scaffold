import os
import os.path as xpath
from typing import Union

TPath = Union[os.PathLike, str]


class HotLoader:
    # loader_filename: str = 'HotLoader.qml'
    cache_dirname: str
    bootloader: TPath
    target: TPath
    
    def __init__(self, cache_dirname='__declare_qml__'):
        self.cache_dirname = cache_dirname
        self.bootloader = xpath.abspath(
            f'{__file__}/../view.qml'
        )
        assert xpath.exists(self.bootloader)
    
    def _check_bootloader_location(self, target: TPath):
        """
        Args:
            target: filepath to *.qml.
        
        Notes:
            我们需要准备一个 HotLoader.qml 文件, 和一个 target (.qml) 文件.
            `class:HotLoader` 会先加载 HotLoader.qml, 然后再通过 HotLoader.qml
            加载 target 文件.
            其中, HotLoader.qml 文件由本模块所在的目录下的 './LKLogger
            /HotLoader.qml' 提供; target 由用户在 `self.start` 处传入.
            
            这里有一个注意事项, target 必须使用相对路径 (相对于
            'HotLoader.qml'), 不能使用绝对路径. 否则会导致 target 文件中的所有
            relative import 语句全部无法正常工作.
            当 target 与 HotLoader.qml 同盘符时, 使用 `xpath.relpath` 即可计算
            出此相对路径. 但是二者不同盘符时, 无法使用 `xpath.relpath` 计算.
            我们的解决方法是, 复制一个 HotLoader.qml 文件到与 target 同目录下的
            `~/{self.cache_dirname}/HotLoader.qml` 路径.
        """
        # 1
        target = xpath.abspath(target)
        if self.bootloader[0] == target[0]:
            return
        
        # 2
        new_bootloader = xpath.join(
            xpath.dirname(target), self.cache_dirname, 'view.qml'
        )
        if xpath.exists(new_bootloader):
            return
        
        # 3
        from lk_logger import lk
        lk.logt(
            '[W2413]',
            'The target qml locates in a different driver with `declare_pyside'
            '.qmlside.LKLogger.HotLoader`, we will make a copy of "HotLoader'
            '.qml" in target directory:\n\t{}'.format(new_bootloader),
            h='grand_parent'
        )
        
        new_bootloader_dir = xpath.dirname(new_bootloader)
        if not xpath.exists(new_bootloader_dir):
            os.mkdir(new_bootloader_dir)
        
        from shutil import copyfile
        copyfile(self.bootloader, new_bootloader)
        
        self.bootloader = new_bootloader
    
    def start(self, target: TPath):
        self._check_bootloader_location(target)
        
        # FIXME
        # # self.target = xpath.relpath(
        # #     target, xpath.dirname(self.bootloader)
        # # )
        self.target = 'file:///' + xpath.abspath(target)
        
        # register hot reloader runtime functions.
        # see usages in `..LKQmSide.HotLoader`.
        from ...pyside import app
        from ...pyside import pyside
        pyside.register(app.engine.clearComponentCache,
                        '__clear_component_cache')
        pyside.register(self.get_target,
                        '__get_target_to_load')
        
        # start app
        app.start(self.bootloader)
    
    def get_target(self):
        return self.target


hot_loader = HotLoader()
