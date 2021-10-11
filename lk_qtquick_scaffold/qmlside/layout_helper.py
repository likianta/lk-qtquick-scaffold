from PySide6.QtCore import QObject
from PySide6.QtCore import Slot

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


class LKLayoutHelper(QObject):
    
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
            js_eval.eval_js(
                '{{0}}.anchors.marginLeft = {}'.format(padding),
                children[0]
            )
            js_eval.eval_js(
                '{{0}}.anchors.marginRight = {}'.format(padding),
                children[-1]
            )
        else:
            js_eval.eval_js(
                '{{0}}.anchors.marginTop = {}'.format(padding),
                children[0]
            )
            js_eval.eval_js(
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
                js_eval.eval_js('{0}.anchors.leftMargin', spacing)
    
    @Slot(QObject, int, int)
    def halign_children(self, parent: QObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, HORIZONTAL)
    
    @Slot(QObject, int, int)
    def valign_children(self, parent: QObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, VERTICAL)
