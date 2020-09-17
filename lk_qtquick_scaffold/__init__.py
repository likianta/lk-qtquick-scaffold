"""
@Author   : dingxianjie (likianta@foxmail.com)
@FileName : __init__.py
@Version  : 0.1.0
@Created  : 2020-09-15
@Updated  : 2020-09-15
@Desc     : 通过导入 lk_qtquick_scaffold, 获得全局变量 app, pyhooks 和 qthooks.
    Usage:
        # === my_launcher.py ===
        from lk_qtquick_scaffold import init_app
        import submodule
        
        if __name__ == '__main__':
            my_app = init_app()
            my_app.start()
            submodule.main()
            
        # === submodule.py ===
        def main():
            from lk_qtquick_scaffold import app, pyhooks, qthooks
            model = qthooks.update(
                'qml/Main.qml#_listModel', 'model', ['a', 'b', 'c']
            )
"""
from launcher import Application
from pycomm import PyHooks, QtHooks

__version__ = '0.1.0'

app: Application
pyhooks: PyHooks
qthooks: QtHooks


def init_app(entrance, *lib, **kwargs):
    """ Init app at program starts. """
    global app, pyhooks, qthooks
    
    app = Application(entrance, *lib, **kwargs)
    
    pyhooks = PyHooks()
    qthooks = QtHooks(app.engine, pyhooks)
    
    app.register_pyhandler('PyHooks', pyhooks)
    app.register_pyhandler('QtHooks', qthooks)
    
    return app
