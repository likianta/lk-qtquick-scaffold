"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : pyhandler.py
@Created : 2020-08-31
@Updated : 2020-09-17
@Version : 0.0.4
@Desc    : 
"""
from PySide2.QtCore import Slot

from _typing import *


class PyHandler(QObject):
    
    @Slot(str, QVal, QUid)
    @Slot(str, QVal)
    @Slot(str, QUid)
    @Slot(str)
    def main(self, method: str, params: QVal = None, uid: QUid = ''):
        try:
            if params is None:
                eval(f'self.{method}()')
            else:
                eval(f'self.{method}(params.toVariant())')
        except Exception as e:
            raise Exception('PyHandler executing error at "{}"'.format(uid), e)
        
    def update_list_model(self, uid, ):
        pass
