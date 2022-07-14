from qtpy.QtCore import QObject
from typing import Iterator


def get_children(qobject: QObject) -> Iterator[QObject]:
    for i in qobject.children():
        if i.property('enabled') is None:
            continue
        yield i
