from typing import *

from PySide6.QtCore import QObject
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue

from .js_evaluator import eval_js
from .js_evaluator import js_eval

# orientation
HORIZONTAL = 0
VERTICAL = 1

# text alignment
H_LEFT = 1
H_CENTER = 4
H_RIGHT = 2
V_TOP = 32
V_CENTER = 128
V_BOTTOM = 64


class T:  # TypeHint
    class Anchors(TypedDict):
        # { 'reclines': tuple[left, top, right, bottom],
        #   'margins': Union[tuple[left, top, right, bottom], int] }
        #   note: `reclines = (0, 0, 0, 0)` means anchorin center.
        reclines: Union[tuple[int, int, int, int], tuple[bool, bool, bool, bool]]
        margins: Union[int, tuple[int, int, int, int]]


class LKLayoutHelper(QObject):
    
    @Slot(QObject, QObject, QJSValue)
    def quick_anchors(self, qobj: QObject, parent: QObject, anchors: T.Anchors):
        # noinspection PyUnresolvedReferences
        anchors = anchors.toVariant()
        
        match anchors['reclines']:
            case (0, 0, 0, 0):
                eval_js('{}.anchors.centerIn = {}', qobj, parent)
            case (1, 1, 1, 1):
                eval_js('{}.anchors.fill = {}', qobj, parent)
            case _:
                if anchors['reclines'][0]:
                    eval_js(
                        '{}.anchors.left = Qt.binding(() => {}.left)',
                        qobj, parent
                    )
                if anchors['reclines'][1]:
                    eval_js(
                        '{}.anchors.top = Qt.binding(() => {}.top)',
                        qobj, parent
                    )
                if anchors['reclines'][2]:
                    eval_js(
                        '{}.anchors.right = Qt.binding(() => {}.right)',
                        qobj, parent
                    )
                if anchors['reclines'][3]:
                    eval_js(
                        '{}.anchors.bottom = Qt.binding(() => {}.bottom)',
                        qobj, parent
                    )
        
        if isinstance((m := anchors['margins']), int):
            eval_js('{}.anchors.margins = {}', qobj, m)
        else:
            eval_js('{}.anchors.leftMargin = {}', qobj, anchors['margins'][0])
            eval_js('{}.anchors.topMargin = {}', qobj, anchors['margins'][1])
            eval_js('{}.anchors.rightMargin = {}', qobj, anchors['margins'][2])
            eval_js('{}.anchors.bottomMargin = {}', qobj, anchors['margins'][3])
    
    @Slot(QObject, str)
    def quick_align(self, qobj: QObject, alignment: str):
        def _normalize_alignment(alignment: str):
            for k, v in {
                'center' : (H_CENTER, V_CENTER),
                'hcenter': (H_CENTER, V_TOP),
                'vcenter': (H_LEFT, V_CENTER)
            }.items():
                if alignment == k:
                    return v
            
            # noinspection PyUnusedLocal
            final_h = final_v = None
            
            for k, v in {
                'l'    : H_LEFT,
                'left' : H_LEFT,
                'r'    : H_RIGHT,
                'right': H_RIGHT,
            }.items():
                if alignment.startswith(k):
                    final_h = v
                    alignment = alignment.removeprefix(k)
                    break
            
            alignment = alignment.lstrip('-')
            
            for k, v in {
                't'     : V_TOP,
                'top'   : V_TOP,
                'b'     : V_BOTTOM,
                'bottom': V_BOTTOM,
                'center': V_CENTER,
            }.items():
                if alignment.startswith(k):
                    final_v = v
                    return final_h, final_v
            
            raise Exception('Illegal alignment', alignment)
        
        h, v = _normalize_alignment(alignment)
        qobj.setProperty('horizontalAlignment', h)
        qobj.setProperty('verticalAlignment', v)
    
    @staticmethod
    def _align_children(parent: QObject, padding: int, spacing: int, orientation: int):
        children = parent.children()
        if len(children) == 0:
            return
        
        if orientation == HORIZONTAL:
            eval_js(
                '{{0}}.anchors.marginLeft = {}'.format(padding),
                children[0]
            )
            eval_js(
                '{{0}}.anchors.marginRight = {}'.format(padding),
                children[-1]
            )
        else:
            eval_js(
                '{{0}}.anchors.marginTop = {}'.format(padding),
                children[0]
            )
            eval_js(
                '{{0}}.anchors.marginBottom = {}'.format(padding),
                children[-1]
            )
        
        prop = 'width' if orientation == HORIZONTAL else 'height'
        size = (
                parent.property(prop)
                - padding * 2
                - spacing * (len(children) - 1)
        )
        
        for i in children:
            i.setProperty(prop, size)
        
        if len(children) > 1:
            for a, b in zip(children[:-1], children[1:]):
                js_eval.bind_anchors(b, 'anchors.left', a, 'right')
                eval_js('{0}.anchors.leftMargin', spacing)
    
    @Slot(QObject, int, int)
    def halign_children(self, parent: QObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, HORIZONTAL)
    
    @Slot(QObject, int, int)
    def valign_children(self, parent: QObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, VERTICAL)
