"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : pyhandler.py
@Created : 2020-08-31
@Updated : 2020-09-17
@Version : 0.0.5
@Desc    : 
"""
from PySide2.QtCore import Slot

from _typing import *


class PyHandler(QObject):
    
    def __init__(self):
        super().__init__()
        self.__pymethods_dict = {}
    
    @Slot(str, QVal, QUid)
    @Slot(str, QVal)
    @Slot(str, QUid)
    @Slot(str)
    def main(self, method: str, params: QVal = None, uid: QUid = ''):
        try:
            if params is None:
                self.__pymethods_dict.get(method, self._invalid_method)()
            else:
                # noinspection PyArgumentList
                self.__pymethods_dict.get(method, self._invalid_method)(
                    params.toVariant()
                )
        except Exception as e:
            raise Exception('PyHandler executing error at "{}"'.format(uid), e)
    
    def register_pymethod(self, func: staticmethod):
        self.__pymethods_dict[func.__name__] = func
    
    def _invalid_method(self, *args):
        return
    
    def update_list_model(self, uid, ):
        pass


if __name__ == '__main__':
    def _xxx():
        print('hi')
    
    
    handler = PyHandler()
    handler.register_pymethod(_xxx)
    handler.main('_xxx')
