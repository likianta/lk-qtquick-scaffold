from typing import *

from PySide6.QtCore import QObject
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue

from .externals import eval_js


class T:  # TypeHint
    
    class Anchors(TypedDict):
        reclines: Union[tuple[int, int, int, int], str]
        #   examples:
        #       (1, 0, 1, 1): left(on), top(off), right(on), bottom(on).
        #       'ijkl': i=top, k=bottom, j=left, l=right.
        #   special values:
        #       (0, 0, 0, 0): center in parent.
        #       (1, 1, 1, 1): fill parent.
        #       'center': center in parent.
        #       'fill': fill parent.
        margins: Union[int, tuple[int, int, int, int]]
    
    Reclines = tuple[int, int, int, int]


class Anchors:
    
    @staticmethod
    def _normalize_reclines(reclines) -> T.Reclines:
        if isinstance(reclines, str):
            match reclines:
                case 'center':
                    return 0, 0, 0, 0
                case 'fill':
                    return 1, 1, 1, 1
                case _:
                    def _foo(letter) -> int:
                        if f'-{letter}' in reclines:
                            return -1
                        elif letter in reclines:
                            return 1
                        else:
                            return 0

                    # noinspection PyTypeChecker
                    return tuple(map(_foo, ('j', 'i', 'l', 'k')))
        else:
            return reclines
    
    @Slot(QObject, QObject, QJSValue)
    def weak_anchors(self, qobj: QObject, parent: QObject, anchors: T.Anchors):
        # noinspection PyUnresolvedReferences
        anchors = anchors.toVariant()
        
        reclines = self._normalize_reclines(anchors['reclines'])
        x = y = w = h = 0
        is_center_mode = False
        
        if all(reclines):
            x = parent.property('x')
            y = parent.property('y')
            w = parent.property('width')
            h = parent.property('height')
        elif not any(reclines):
            is_center_mode = True
            x = parent.property('width') / 2 - qobj.property('width') / 2
            y = parent.property('height') / 2 - qobj.property('height') / 2
            w = qobj.property('width')
            h = qobj.property('height')
        else:
            if reclines[0]:
                if reclines[0] > 0:
                    x = parent.property('x')
                else:
                    x = parent.property('x') + parent.property('width')
            if reclines[1]:
                if reclines[1] > 0:
                    y = parent.property('y')
                else:
                    y = parent.property('y') + parent.property('height')
            if reclines[2]:
                if reclines[2] > 0:
                    w = parent.property('width')
                else:
                    w = parent.property('x') + parent.property('width') - x
            if reclines[3]:
                if reclines[3] > 0:
                    h = parent.property('height')
                else:
                    y = parent.property('y') + parent.property('height') - y
        
        if not is_center_mode:
            
            margins = anchors['margins']
            
            if isinstance(margins, int):
                x += margins
                y += margins
                w -= margins
                h -= margins
            else:
                x += margins[0]
                y += margins[1]
                w -= margins[2]
                h -= margins[3]
        
        qobj.setProperty('x', x)
        qobj.setProperty('y', y)
        qobj.setProperty('width', w)
        qobj.setProperty('height', h)
    
    @Slot(QObject, QObject, QJSValue)
    def quick_anchors(self, qobj: QObject, parent: QObject, anchors: T.Anchors):
        # noinspection PyUnresolvedReferences
        anchors = anchors.toVariant()
        
        def _normalize_reclines(reclines) -> T.Reclines:
            if isinstance(reclines, str):
                match reclines:
                    case 'center':
                        return 0, 0, 0, 0
                    case 'fill':
                        return 1, 1, 1, 1
                    case _:
                        return (
                            'j' in reclines,  # j=left
                            'i' in reclines,  # i=top
                            'l' in reclines,  # l=right
                            'k' in reclines,  # k=bottom
                        )
            else:
                return reclines
        
        reclines = _normalize_reclines(anchors['reclines'])
        
        if all(reclines):
            eval_js('{}.anchors.fill = {}', qobj, parent)
        elif not any(reclines):
            eval_js('{}.anchors.centerIn = {}', qobj, parent)
        else:
            if reclines[0]:
                if reclines[0] > 0:
                    eval_js(
                        '{}.anchors.left = Qt.binding(() => {}.left)',
                        qobj, parent
                    )
                else:
                    eval_js(
                        '{}.anchors.left = Qt.binding(() => {}.right)',
                        qobj, parent
                    )
            if reclines[1]:
                if reclines[1] > 0:
                    eval_js(
                        '{}.anchors.top = Qt.binding(() => {}.top)',
                        qobj, parent
                    )
                else:
                    eval_js(
                        '{}.anchors.top = Qt.binding(() => {}.bottom)',
                        qobj, parent
                    )
            if reclines[2]:
                if reclines[2] > 0:
                    eval_js(
                        '{}.anchors.right = Qt.binding(() => {}.right)',
                        qobj, parent
                    )
                else:
                    eval_js(
                        '{}.anchors.right = Qt.binding(() => {}.left)',
                        qobj, parent
                    )
            if reclines[3]:
                if reclines[3] > 0:
                    eval_js(
                        '{}.anchors.bottom = Qt.binding(() => {}.bottom)',
                        qobj, parent
                    )
                else:
                    eval_js(
                        '{}.anchors.bottom = Qt.binding(() => {}.top)',
                        qobj, parent
                    )
        
        margins = anchors['margins']
        
        if isinstance(margins, int):
            eval_js('{}.anchors.margins = {}', qobj, margins)
        else:
            eval_js('{}.anchors.leftMargin = {}', qobj, margins[0])
            eval_js('{}.anchors.topMargin = {}', qobj, margins[1])
            eval_js('{}.anchors.rightMargin = {}', qobj, margins[2])
            eval_js('{}.anchors.bottomMargin = {}', qobj, margins[3])
