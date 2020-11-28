"""
@Author  : likianta <likianta@foxmail.com>
@Module  : debugger.py
@Created : 2020-09-20
@Updated : 2020-11-28
@Version : 0.2.1
@Desc    :
"""
from os.path import abspath
from lk_qtquick_scaffold import app, pyhandler


def main():
    pyhandler.register_pyfunc(app.engine.clearComponentCache,
                              'clear_component_cache')
    pyhandler.register_pyfunc(get_target)

    app.start(abspath('./HotReloader.qml'))
    
    
def get_target():
    from platform import system
    if system() == 'Windows':
        return 'file:///' + abspath('../tests/qml/view.qml')
    else:
        return abspath('../tests/qml/view.qml')


if __name__ == '__main__':
    main()
