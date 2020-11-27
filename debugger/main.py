"""
@Author  : likianta <likianta@foxmail.com>
@Module  : debugger.py
@Created : 2020-09-20
@Updated : 2020-11-27
@Version : 0.2.0
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
    # return 'file:///' + abspath('../tests/qml/view.qml')
    from os.path import exists
    print(exists(abspath('../tests/qml/view.qml')))
    return abspath('../tests/qml/view.qml')


if __name__ == '__main__':
    main()
