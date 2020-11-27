"""
@Author   : likianta (likianta@foxmail.com)
@FileName : __init__.py
@Version  : 0.2.2
@Created  : 2020-09-15
@Updated  : 2020-11-27
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

app = Application()
pyhandler = PyHandler()
