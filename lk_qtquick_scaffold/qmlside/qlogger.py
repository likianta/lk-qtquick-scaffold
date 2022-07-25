from os import getcwd
from os.path import abspath
from os.path import relpath

from qtpy.QtCore import QMessageLogContext
from qtpy.QtCore import QtCriticalMsg
from qtpy.QtCore import QtMsgType
from qtpy.QtCore import QtWarningMsg
from qtpy.QtCore import qInstallMessageHandler

_IGNORE_UNPLEASENT_WARNINGS = False


def setup(ignore_unpleasent_warnings=False):
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
    global _IGNORE_UNPLEASENT_WARNINGS
    _IGNORE_UNPLEASENT_WARNINGS = ignore_unpleasent_warnings
    qInstallMessageHandler(_log)


# noinspection PyUnusedLocal
def _log(mode: QtMsgType, ctx: QMessageLogContext, msg: str) -> None:
    """
    Features:
        1. Output stream via PyCharm console.
        2. Support source map print.
    
    References:
        https://stackoverflow.com/questions/53991306/pyside-how-to-see-qml
            -errors-in-python-console
        
    Args:
        mode: qtpy.QtCore.QtMsgType
            There're six message types:
                QtCriticalMsg  # 1
                QtDebugMsg
                QtFatalMsg
                QtInfoMsg
                QtSystemMsg
                QtWarningMsg  # 2
            #1 and #2 are what we mostly occurred.
        ctx: qtpy.QtCore.QMessageLogContext. (ctx: 'context')
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
    
    if _IGNORE_UNPLEASENT_WARNINGS:
        if filename in (
                # https://forum.qt.io/topic/131823/lots-of-typeerrors-in-console
                # -when-migrating-to-qt6/2
                '<qrc:/qt-project.org/imports/QtQuick/Controls/'
                'macOS/Button.qml>',
        ):
            return
    
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
    
    from lk_logger import default_print
    default_print('{}:{}'.format(filename, lineno),
                  ctx.function, msg, sep='\t>>\t')


_dir = getcwd()


def _use_relpath(path: str) -> str:
    """ convert absolute path to relative.
    
    args:
        path: str qml file path.
            currently we've found 2 forms:
                1. file:///c:/workspace/...
                2. c:%5Cworkspace%5C...
                     ^^^         ^^^
    
    warning:
        the path may include '../' in the middle part:
            file:///c:/workspace/../ui/view.qml
                                 ^^^
    
    note:
        to compilance with lk_logger's relpath form, we suggest adding './' to
        the beginning of the path.
    """
    # print(':v', path)
    
    if path.startswith('file:///'):
        path = abspath(path[8:])
        path = relpath(path, _dir).replace('\\', '/')
        if not path.startswith('../'):
            path = './' + path
        return path
    
    elif path.startswith('file://'):  # macos/linux
        path = abspath('/' + path[7].upper() + path[8:])
        #   'file://users/...' -> '/Users/...'
        if path.split('/', 2)[1] == _dir.split('/', 2)[1]:
            path = relpath(path, _dir)
            if not path.startswith('../'):
                path = './' + path
        return path
    
    elif path[1:].startswith(':%5C'):
        return path.replace('%5C', '/')
    
    else:
        # # raise ValueError('Unknown path type', path)
        return f'<{path}>'  # e.g. '<eval code>'
