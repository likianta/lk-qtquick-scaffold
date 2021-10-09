from os import getcwd
from os.path import abspath
from os.path import relpath

from PySide6.QtCore import QtCriticalMsg
from PySide6.QtCore import QtWarningMsg
from PySide6.QtCore import qInstallMessageHandler


def setup():
    """ Print QML runtime info in Python (PyCharm) console.
    
    Motivation:
        In traditional way when we are developing and debugging QML in PyCharm,
        we have to enable 'Toolbar > Edit Run/Debug configurations dialog >
        Emulate terminal in output console' to see `console.log(...)` via
        PyCharm console.
        The disadvantages are that the steps are trivial and enabling it will
        cause PyCharm console loses some features like code highlighting and
        linking etc.
        So we find another way to introduce qml to use the same output stream
        with python print. Just call this function and all work is done.
        
    Notes:
        Call this function before application starts.
    """
    qInstallMessageHandler(_log)


# noinspection PyUnusedLocal
def _log(mode, ctx, msg: str):
    """
    Features:
        1. Output stream via PyCharm console.
        2. Support source map print.
    
    References:
        https://stackoverflow.com/questions/53991306/pyside-how-to-see-qml
            -errors-in-python-console
        
    Args:
        mode: PySide6.QtCore.QtMsgType
            There're six message types:
                QtCriticalMsg  # 1
                QtDebugMsg
                QtFatalMsg
                QtInfoMsg
                QtSystemMsg
                QtWarningMsg  # 2
            #1 and #2 are what we mostly occurred.
        ctx: PySide6.QtCore.QMessageLogContext. (ctx: 'context')
            Context indicates to the place where `console.log` is called or
            where runtime errors happened.
            ctx.file: Optional[str].
                the abspath of file, starts with 'file:///', and usually ends
                with '.qml' or '.js'.
            ctx.line: int.
                the line number, starts from 1.
                sometimes it is -1.
            ctx.function: Optional[str].
                `None` means no function name.
            ctx.category: str.
                *don't know what it is, usually seen its value is 'default' or
                'qml'.*
            ctx.version: int.
                *don't know what it is, usually seen its value is integer 2.*
        msg: str. (msg: 'message')
        
    Returns:
        print: '{file}:{lineno}  >>  {function}  >>  {message}'
    """
    # filename
    filename = _use_relpath(ctx.file) if ctx.file else '<unknown_source>'
    
    # line number
    lineno = 0 if ctx.line == -1 else ctx.line
    
    # function
    function = ctx.function if ctx.function else '<null>'
    
    # optimize msg
    if mode in (QtWarningMsg, QtCriticalMsg):
        if ctx.file and msg.startswith(ctx.file):
            # examples:
            #   msg = '<ctx.file>: <message>'
            #   msg = '<ctx.file>:<line_no>:<column_no>: <message>'
            # so we firstly strip `ctx.file`, then split by ': ' to extract the
            # main message.
            msg = msg[len(ctx.file):].split(': ', 1)[1]
        msg = '\033[31m' + msg + '!' + '\033[0m'
        #   change font color to red, and add an exclamation mark to it.
    
    print('{}:{}'.format(filename, lineno), ctx.function, msg, sep='\t>>\t')


_dir = getcwd()


def _use_relpath(path: str) -> str:
    """ Convert absolute path to relative path.
    
    Args:
        path: currently found 2 types of paths:
            1. 'file:///d:/workspacce/dev_master_likianta/declare_qml/...'
            2. 'd:%5Cworkspace%5Cdev_master_likianta%5Cdeclare_qml%5C...'
                  ^^^         ^^^                   ^^^           ^^^
    
    IN: 'file:///c:/program files/programs/python/Python39/lib/site-packages/lk
        _qtquick_scaffold/debugger/LKDebugger/../../../../../../../../workspace
        /myprj/ui/view.qml'
    OUT: 'ui/view.qml' (relative to current working dir)
    """
    if path.startswith('file:///'):
        path = abspath(path[8:])
        #   'file:///c:/program files/programs/python/Python39/lib/site
        #   -packages/lk_qtquick_scaffold/debugger/LKDebugger/../../../../../../
        #   ../../workspace/myprj/ui/view.qml'
        #   -> 'c:/program files/programs/python/Python39/lib/site-packages/lk_
        #       qtquick_scaffold/debugger/LKDebugger/../../../../../../../../
        #       workspace/myprj/ui/view.qml'
        #   -> 'c:/program files/workspace/myprj/ui/view.qml'
        path = relpath(path, _dir)
        #   launch_dir = 'c:/program files/workspace/myprj'
        #   -> 'ui/view.qml' (or maybe 'ui\\view.qml')
        return path.replace('\\', '/')
        # # return path
    
    elif path[1:].startswith(':%5C'):
        return path.replace('%5C', '/')
    
    else:
        # raise ValueError('Unknown path type', path)
        return f'<{path}>'  # e.g. '<eval code>'
