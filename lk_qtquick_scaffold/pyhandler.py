"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : pyhandler.py
@Created : 2020-08-31
@Updated : 2020-09-15
@Version : 0.0.3
@Desc    : 
"""
from PySide2.QtCore import Slot

from _typing import *


class PyHandler(QObject):
    
    @Slot(str, QUid)
    @Slot(str)
    def main(self, method: str, uid: QUid = ''):
        try:
            eval(f'self.{method}()')
        except Exception as e:
            raise Exception('PyHandler executing error at "{}"'.format(uid), e)
        
    def update_list_model(self, uid, ):
        pass
