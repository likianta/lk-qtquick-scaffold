from PySide6.QtCore import QObject


def get_children(qobject: QObject) -> QObject:
    for i in qobject.children():
        if i.property('enabled') is None:
            continue
        yield i
