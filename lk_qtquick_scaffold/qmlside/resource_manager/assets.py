from os import listdir

from .base import ResourceManager
from ... import path_model


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
