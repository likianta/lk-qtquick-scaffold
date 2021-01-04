from os import getcwd
from os.path import abspath, relpath

from PySide2.QtCore import QtCriticalMsg, QtWarningMsg

launch_dir = getcwd()


def main():  # call this before application starts
    from PySide2.QtCore import qInstallMessageHandler
    qInstallMessageHandler(log)


# noinspection PyUnusedLocal
def log(mode, ctx, msg):
    """ Show qml console and error info in Python console. You don't need to
        enable 'Emulate terminal in output console' in Pycharm anymore.
    
    Pros:
        1. 不需要启用 Pycharm 的 'Emulate terminal in output console' 选项
        2. 支持打印源码位置
    
    References:
        https://stackoverflow.com/questions/53991306/pyside-how-to-see-qml
        -errors-in-python-console
        
    Args:
        mode: PySide2.QtCore.QtMsgType
            There're 6 msg types:
                QtCriticalMsg: 以红色字体显示, 并在 msg 末尾加一个叹号
                QtDebugMsg
                QtFatalMsg
                QtInfoMsg
                QtSystemMsg
                QtWarningMsg: 以红色字体显示, 并在 msg 末尾加一个叹号
        ctx: PySide2.QtCore.QMessageLogContext. 'context'.
                Context indirects to the place where `console.log` is called or
                where runtime errors happend.
            ctx.file: shows the abspath of file, startswith 'file:///', and
                usually endswith '.qml' or '.js'.
            ctx.line: shows the line number, startswith 1.
            ctx.function: str|None. None means no function name
            ctx.category: 'qml'
            ctx.version: int (always to 2 in lk_qtquick_scaffold)
        msg: str. 'message'
        
    Returns:
        print: '{file}:{line_number}  >>  {function}  >>  {message}'
    """
    if mode in (QtWarningMsg, QtCriticalMsg):
        msg = msg.split(': ', 1)[1]
        #   msg = 'file:///a_very_long_path.qml:1: ReferenceError...'
        #   -> 'ReferenceError...'
        #       Why strip the filepath in msg? -- 1. the path is very long and
        #       unreadable; 2. the path is duplicated to ctx.file, which we've
        #       already optimized and provided by `simple_path`.
        msg = '\033[31m' + msg + '!' + '\033[0m'
        #   Change font color to red, and add an exclamation mark to it
    if msg.endswith('sourcemap=false'):
        print(msg[:-len('sourcemap=false')])
    else:
        print('{}:{}'.format(simple_path(ctx.file), ctx.line), ctx.function,
              msg, sep='\t>>\t')


def simple_path(path):
    """ Convert absolute path to relative path.
    
    IO: 'file:///c:/program files/programs/python/Python39/lib/site-packages/lk_
        qtquick_scaffold/debugger/LKDebugger/../../../../../../../../workspace/
        myprj/ui/view.qml'
        -> 'ui/view.qml' (relative to '~/myprj')
    """
    path = abspath(path[8:])
    #   'file:///c:/program files/programs/python/Python39/lib/site-packages/lk_
    #   qtquick_scaffold/debugger/LKDebugger/../../../../../../../../workspace/
    #   myprj/ui/view.qml'
    #   -> 'c:/program files/programs/python/Python39/lib/site-packages/lk_
    #       qtquick_scaffold/debugger/LKDebugger/../../../../../../../../
    #       workspace/myprj/ui/view.qml'
    #   -> 'c:/program files/workspace/myprj/ui/view.qml'
    path = relpath(path, launch_dir)
    #   launch_dir = 'c:/program files/workspace/myprj'
    #   -> 'ui/view.qml' (or maybe 'ui\\view.qml')
    return path.replace('\\', '/')
