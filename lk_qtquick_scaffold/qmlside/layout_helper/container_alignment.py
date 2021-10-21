from textwrap import dedent
from textwrap import indent

from PySide6.QtCore import QObject
from PySide6.QtCore import Slot

from ._ext import *

HORIZONTAL = 0
VERTICAL = 1


class ContainerAlignment:
    
    @Slot(QObject)
    @adapt_argtypes
    def fill_width(self, parent: TQObject):
        self._fill_size(parent, HORIZONTAL)
    
    @Slot(QObject)
    @adapt_argtypes
    def fill_height(self, parent: TQObject):
        self._fill_size(parent, VERTICAL)
    
    def _fill_size(self, parent: TQObject, orientation: int):
        paddings = self._get_paddings(parent)
        if orientation == HORIZONTAL:
            prop_name = 'width'
            padding = paddings[0] + paddings[2]
        else:
            prop_name = 'height'
            padding = paddings[1] + paddings[3]
        
        for item in parent.get_children():
            size = item.property(prop_name)
            if size >= 1:
                continue
            elif 0 < size < 1:
                ratio = size
            elif size == 0:
                ratio = 1
            else:
                raise ValueError(size)
            
            js_eval.quick_bind(
                item, prop_name,
                parent, '{} * {} - {}'.format(
                    prop_name, ratio, padding
                )
            )
    
    # --------------------------------------------------------------------------
    
    @Slot(QObject)
    @adapt_argtypes
    def halign_center(self, parent: TQObject):
        """ Align children in a horizontal line. """
        for item in parent.get_children():
            eval_js('{}.anchors.verticalCenter '
                    '= Qt.binding(() => {}.verticalCenter)',
                    item, parent)
    
    @Slot(QObject)
    @adapt_argtypes
    def valign_center(self, parent: TQObject):
        """ Align children in a vertical line. """
        for item in parent.get_children():
            eval_js('{}.anchors.horizontalCenter '
                    '= Qt.binding(() => {}.horizontalCenter)',
                    item, parent)
    
    # --------------------------------------------------------------------------
    
    @Slot(QObject, int, int)
    @adapt_argtypes
    def halign_children(self, parent: TQObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, HORIZONTAL)
    
    @Slot(QObject, int, int)
    @adapt_argtypes
    def valign_children(self, parent: TQObject, padding: int, spacing: int):
        self._align_children(parent, padding, spacing, VERTICAL)
    
    @staticmethod
    def _align_children(parent: TQObject, padding: int, spacing: int,
                        orientation: int):
        children = list(parent.get_children())
        if len(children) == 0:
            return
        
        if orientation == HORIZONTAL:
            eval_js(
                '{{0}}.anchors.leftMargin = {}'.format(padding),
                children[0]
            )
            eval_js(
                '{{0}}.anchors.rightMargin = {}'.format(padding),
                children[-1]
            )
        else:
            eval_js(
                '{{0}}.anchors.topMargin = {}'.format(padding),
                children[0]
            )
            eval_js(
                '{{0}}.anchors.bottomMargin = {}'.format(padding),
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
                js_eval.quick_bind(b, 'anchors.left', a, 'right')
                eval_js('{0}.anchors.leftMargin', spacing)
    
    # --------------------------------------------------------------------------
    
    @Slot(QObject)
    @Slot(QObject, bool)
    @adapt_argtypes
    def hadjust_children_size(self, parent: TQObject, constraint=True):
        self._auto_adjust_children_size(parent, HORIZONTAL, constraint)
    
    @Slot(QObject)
    @Slot(QObject, bool)
    @adapt_argtypes
    def vadjust_children_size(self, parent: TQObject, constraint=True):
        self._auto_adjust_children_size(parent, VERTICAL, constraint)
    
    def _auto_adjust_children_size(
            self, parent: TQObject, orientation: int, constraint: bool
    ):
        def _adjust(prop_name, unallocated_space):
            dynamic_sized_items_a = []  # type: List[Tuple[QObject, float]]
            dynamic_sized_items_b = []  # type: List[Tuple[QObject, float]]
            
            for i, item in enumerate(children):
                size = item.property(prop_name)
                if 0 < size < 1:
                    dynamic_sized_items_a.append((item, size))
                elif size == 0:
                    dynamic_sized_items_b.append((item, size))
                else:
                    unallocated_space -= size
            
            # ------------------------------------------------------------------
            
            if not dynamic_sized_items_a + dynamic_sized_items_b:
                return
            if unallocated_space <= 0:
                raise Exception('No space for allocating left children')
            if (declared_ratio := sum(x[1] for x in dynamic_sized_items_a)) > 1:
                raise Exception('The total size of dynamic items exceed '
                                'available space', declared_ratio,
                                unallocated_space)
            if declared_ratio == 1 and dynamic_sized_items_b:
                raise Exception('Cannot make space for size-undeclared items')
            
            if dynamic_sized_items_b:
                default_size_for_undefined_items = (
                        (1 - declared_ratio) / len(dynamic_sized_items_b)
                )
                dynamic_sized_items_b = [
                    (item, default_size_for_undefined_items)
                    for item, _ in dynamic_sized_items_b
                ]
            
            for item, ratio in dynamic_sized_items_a + dynamic_sized_items_b:
                if not constraint:
                    item.setProperty(prop_name, unallocated_space * ratio)
                else:
                    eval_js(dedent('''
                        {{0}}.{prop_name} = Qt.binding(() => {{{{
                            {js_expression}
                        }}}})
                    ''').format(
                        prop_name=prop_name,
                        js_expression=indent(dedent('''
                            let unallocated_space =
                                {{1}}.{prop_name} - {fixed_used_size}
                            return unallocated_space * {ratio}
                        '''.format(
                            prop_name=prop_name,
                            fixed_used_size=(parent.property(prop_name)
                                             - unallocated_space),
                            ratio=ratio,
                        )), ' ' * 4).strip()
                    ), item, parent)
        
        paddings = self._get_paddings(parent)
        spacing = parent.property('spacing')
        
        children = parent.get_children()
        # lk.logp([x.property('objectName') for x in children])
        
        if orientation == HORIZONTAL:
            _adjust(
                prop_name='width',
                unallocated_space=(
                        parent.property('width')
                        - (paddings[0] + paddings[2])
                        - spacing * (len(children) - 1)
                )
            )
        
        elif orientation == VERTICAL:
            _adjust(
                prop_name='height',
                unallocated_space=(
                        parent.property('height')
                        - (paddings[1] + paddings[3])
                        - spacing * (len(children) - 1)
                )
            )
    
    @staticmethod
    def _get_paddings(qobj: TQObject):
        if p := qobj.property('padding'):
            return p, p, p, p
        else:
            padding_l = qobj.property('leftPadding')
            padding_t = qobj.property('topPadding')
            padding_r = qobj.property('rightPadding')
            padding_b = qobj.property('bottomPadding')
            return padding_l, padding_t, padding_r, padding_b
