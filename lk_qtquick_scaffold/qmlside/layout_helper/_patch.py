from __future__ import annotations

from qtpy.QtCore import QObject


def get_children(qobject: QObject) -> list[QObject]:
    out = []
    for i in qobject.children():
        if i.property('enabled') is None:
            continue
        out.append(i)
    return out
