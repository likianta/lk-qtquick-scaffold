"""
@Author  : likianta <likianta@foxmail.com>
@Module  : debugger.py
@Created : 2020-09-20
@Updated : 2020-11-26
@Version : 0.1.2
@Desc    :
"""
from os.path import abspath


def main():
    from lk_qtquick_scaffold import init_app
    print(abspath('HotReloader.qml'))
    app = init_app(abspath('./HotReloader.qml'))
    
    # A: not work
    #   app.register_pyobj('QmlEngine', app.engine) 
    # B: worked
    from lk_qtquick_scaffold import pyhandler
    pyhandler.register_pymethod(app.engine.clearComponentCache)
    
    app.start()


if __name__ == '__main__':
    import sys
    sys.path.append(abspath('../lk_qtquick_scaffold'))
    # print(sys.path)
    main()
