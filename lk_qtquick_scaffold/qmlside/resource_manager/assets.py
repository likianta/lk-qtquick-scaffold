from os import listdir

from PySide6.QtCore import QUrl

from ._ext import path_model
from .base import ResourceManager


class AssetsResourceManager(ResourceManager):
    assets_dir = path_model.assets_dir
    icons_dir = f'{assets_dir}/icons'
    index: dict
    
    def __init__(self):
        super().__init__()
        self._indexing_assets()
    
    def _indexing_assets(self):
        self.index = {}
        for d in listdir(self.assets_dir):
            for n in listdir(f'{self.assets_dir}/{d}'):
                self.index[n] = f'{self.assets_dir}/{d}/{n}'
    
    def _get(self, name, **kwargs):
        return f'file:///{self.index[name]}'

