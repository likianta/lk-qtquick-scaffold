from __future__ import annotations

from qtpy.QtCore import QObject

from lk_qtquick_scaffold import app
from lk_qtquick_scaffold import slot

__all__ = ['HotReloader']


class HotReloader(QObject):
    
    def __init__(self, title='LK Hot Reloader', reload_scheme='default'):
        """
        args:
            reload_scheme: 'default' or 'clear_cache'
                see its only usage in `def reload`.
        """
        super().__init__(None)
        
        self.source = ''
        self.title = title
        self._loader = None
        self._reload_scheme = reload_scheme
        
        from lk_utils import relpath
        self._view_file = relpath('./view_temp.qml')
        # # self._view_file = relpath('./view.qml')  # TODO: wip
    
    def run(self, file: str):
        from lk_utils.filesniff import normpath
        self.source = 'file:///' + normpath(file, force_abspath=True)
        app.set_app_name(self.title)
        app.register(self, 'pyloader')
        app._run(self._get_bootloader_file(file))  # noqa
    
    def dry_run(self):
        app.register(self, 'pyloader')
        app._run(self._view_file)  # noqa
    
    def _get_bootloader_file(self, target_ref: str) -> str:
        """
        we must put [./view.qml] and [target_ref] under the same hard driver.
        otherwise all relative imports in qml side will be crashed.
        so here we check the bootloader (./view.qml) location's initial letter
        with targets'.
        """
        from lk_utils import dumps
        from os import mkdir
        from os.path import dirname, exists, splitdrive
        from shutil import copyfile
        
        our_view = self._view_file  # this is an absolute path.
        
        if splitdrive(our_view)[0] == splitdrive(target_ref)[0]:
            # note: this is worked on windows; for unix system, they are
            # `'' == ''` (always True).
            return our_view
        
        new_dir = f'{dirname(target_ref)}/__lk_qtquick_scaffold__'
        old_file, new_file = our_view, f'{new_dir}/view.qml'
        print(
            'The target file locates in a different driver with hot '
            'reloader. we will make a copy of reloader\'s "view.qml" in '
            'the same directory of target:\n    {}'.format(new_dir), ':v3p2'
        )
        if not exists(new_dir):
            mkdir(new_dir)
            dumps('Generated by [lk-qtquick-scaffold](https://github.com/'
                  'likianta/lk-qtquick-scaffold)/hot-reloader/hot_reloader/'
                  'main.py : class HotReloader : def _get_bootloader_file',
                  f'{new_dir}/README.md')
        
        copyfile(old_file, new_file)
        return new_file
    
    # -------------------------------------------------------------------------
    
    source: str
    _count: int = -1
    _loader: QObject | None
    
    @slot(object)
    def set_loader(self, loader: QObject):
        self._loader = loader
    
    @slot()
    def reload(self):
        assert self._loader, 'Loader is not set, did you forget to call ' \
                             '`set_loader`?'
        self._count += 1
        
        if self._count == 0:
            # it's the first time to load.
            self._loader.setProperty('source', self.source)
            return
        
        print(':dvs', f'Reload target ({self._count})')
        if self._reload_scheme == 'default':
            # A. use "magic count" to update url but not change the source path.
            self._loader.setProperty(
                'source', self.source + f'?magic_count={self._count}'
            )
        else:
            # B. clear component cache to force reload.
            self._loader.setProperty('source', '')
            app.engine.clearComponentCache()
            self._loader.setProperty('source', self.source)
