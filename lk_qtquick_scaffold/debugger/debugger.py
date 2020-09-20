"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : debugger.py
@Created : 2020-09-20
@Updated : 2020-09-20
@Version : 0.1.1
@Desc    :
"""
from lk_qtquick_scaffold import init_app


def main():
    app = init_app('./HotReloader.qml')
    
    # app.register_pyobj('QmlEngine', app.engine)  # A: not work
    from lk_qtquick_scaffold import pyhandler  # ------------------- B
    pyhandler.register_pymethod(app.engine.clearComponentCache)  # - B
    
    app.start()


main()
