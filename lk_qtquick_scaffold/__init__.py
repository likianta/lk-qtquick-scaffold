"""
@Author   : likianta (likianta@foxmail.com)
@FileName : __init__.py
@Version  : 0.2.3
@Created  : 2020-09-15
@Updated  : 2021-01-04
@Desc     : 通过导入 lk_qtquick_scaffold, 获得全局变量 app, pyhandler.
    
    Usage:
        '''
        |- myprj
            |- control.py
            |- view.qml
        '''
        # control.py
        from lk_qtquick_scaffold import app
        
        if __name__ == '__main__':
            app.start('view.qml')
    
"""
from .launcher import Application
from .pycomm import PyHandler
from .debugger import logger

logger.main()
app = Application()
pyhandler = PyHandler()
