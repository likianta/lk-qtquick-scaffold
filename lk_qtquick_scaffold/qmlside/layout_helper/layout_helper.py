from __future__ import annotations

from functools import partial

from qtpy.QtCore import Property
from qtpy.QtCore import QObject

from ._patch import get_children
from ..js_evaluator import eval_js
from ...pyside import slot


class Enum:  # DELETE
    HORIZONTAL = 0
    VERTICAL = 1
    STRETCH = -1
    SHRINK = -2


class LayoutHelper(QObject):
    HORIZONTAL = Property(int, lambda _: 0, constant=True, final=True)
    VERTICAL = Property(int, lambda _: 1, constant=True, final=True)
    
    @slot(object, str)
    def auto_align(self, container: QObject, alignment: str):
        """
        args:
            alignment: accept multiple options, separated by comma (no space
                between).
                for example: 'hcenter,stretch'
                options list:
                    hcenter: child.horizontalCenter = container.horizontalCenter
                    vcenter: child.verticalCenter = container.verticalCenter
                    hfill: child.with = container.width
                    vfill: child.height = container.height
                    stretch
        """
        children = tuple(get_children(container))
        
        for a in alignment.split(','):
            if a == 'hcenter':
                for child in children:
                    eval_js('''
                        $child.anchors.horizontalCenter = Qt.binding(() => {
                            return $container.horizontalCenter
                        })
                    ''', {'child': child, 'container': container})
            
            elif a == 'vcenter':
                for child in children:
                    eval_js('''
                        $child.anchors.verticalCenter = Qt.binding(() => {
                            return $container.verticalCenter
                        })
                    ''', {'child': child, 'container': container})
            
            elif a == 'hfill' or a == 'vfill':
                def resize_children(orientation: str):
                    nonlocal container
                    prop = 'width' if orientation == 'h' else 'height'
                    for child in get_children(container):
                        child.setProperty(prop, container.property(prop))
                
                if a == 'hfill':
                    container.widthChanged.connect(
                        partial(resize_children, 'h')
                    )
                    container.widthChanged.emit()
                else:
                    container.heightChanged.connect(
                        partial(resize_children, 'v')
                    )
                    container.heightChanged.emit()
            
            elif a == 'stretch':
                container_type = self._detect_container_type(container)
                
                def stretch_children(orientation: str):
                    nonlocal container
                    prop = 'width' if orientation == 'h' else 'height'
                    children = tuple(get_children(container))
                    size_total = (container.property(prop)
                                  - container.property('spacing')
                                  * (len(children) - 1))
                    size_aver = size_total / len(children)
                    # print(':v', prop, size_total, size_aver)
                    for child in get_children(container):
                        child.setProperty(prop, size_aver)
                
                if container_type == 0:
                    container.widthChanged.connect(
                        partial(stretch_children, 'h')
                    )
                    container.widthChanged.emit()
                elif container_type == 1:
                    container.heightChanged.connect(
                        partial(stretch_children, 'v')
                    )
                    container.heightChanged.emit()
    
    @slot(object, int)
    def auto_size_children(self, container: QObject, orientation: int):
        """
        size policy:
            0: auto stretch to spared space.
            0 ~ 1: the ratio of spared space.
            1+: regular pixel point.

        workflow:
            1. get total space
            2. consume used space
            3. allocate unused space

        TODO: method rename (candidate names):
            mobilize
            auto_pack
        """
        prop_name = 'width' if orientation == Enum.HORIZONTAL else 'height'
        if container.property(prop_name) <= 0: return
        children = tuple(get_children(container))
        total_size = self._get_total_available_size_for_children(
            container, len(children), orientation)
        # item_sizes = {}  # dict[int index, float size]
        item_sizes = []  # list[int index]
        
        unclaimed_size = total_size
        for idx, item in enumerate(children):
            size = item.property(prop_name)
            if size < 0:
                raise ValueError('cannot allocate negative size', idx, item)
            if size >= 1:
                item_sizes.append(idx)
                unclaimed_size -= size
        
        def fast_finish_leftovers():
            for idx, item in enumerate(children):
                if idx not in item_sizes:
                    item.setProperty(prop_name, 0)
        
        if unclaimed_size <= 0:
            fast_finish_leftovers()
            return
        
        total_unclaimed_size = unclaimed_size
        for idx, item in enumerate(children):
            size = item.property(prop_name)
            if idx not in item_sizes:
                if 0 < size < 1:
                    ratio = size
                    size = total_unclaimed_size * ratio
                    item.setProperty(prop_name, size)
                    item_sizes.append(idx)
                    unclaimed_size -= size
        
        if unclaimed_size <= 0:
            fast_finish_leftovers()
            return
        
        left_count = len(children) - len(item_sizes)
        left_size_average = unclaimed_size / left_count
        for idx, item in enumerate(children):
            if idx not in item_sizes:
                item.setProperty(prop_name, left_size_average)
        
        print(':d')
        print(':sv2', (container.property('width'), container.property('height')))
        for idx, item in enumerate(children):
            print(idx, item.property('objectName'),
                  (item.property('width'), item.property('height')), ':s')
    
    @staticmethod
    def _get_total_available_size_for_children(
            item: QObject, children_length: int, orientation: int) -> int:
        if orientation == Enum.HORIZONTAL:
            return (
                    item.property('width')
                    - item.property('leftPadding')
                    - item.property('rightPadding')
                    - item.property('spacing') * (children_length - 1)
            )
        else:
            return (
                    item.property('height')
                    - item.property('topPadding')
                    - item.property('bottomPadding')
                    - item.property('spacing') * (children_length - 1)
            )
    
    @slot(list, result=tuple)
    @slot(list, int, result=tuple)
    @slot(list, int, int, result=tuple)
    def calc_text_block_size(
            self, lines: list[str],
            char_width=10, line_height=20
    ):
        lines = tuple(map(str, lines))
        # OPTM: use different char_width for non-ascii characters.
        width = max(map(len, lines)) * char_width
        height = (len(lines) + 1) * line_height
        return width, height
    
    @slot(object, str)
    def equal_size_children(self, container: QObject, orientation: str):
        # roughly equal size children
        children = tuple(get_children(container))
        if orientation in ('horizontal', 'h'):
            prop = 'width'
        else:
            prop = 'height'
        average_size = container.property(prop) / len(children)
        for item in children:
            item.setProperty(prop, average_size)
    
    @staticmethod
    def _detect_container_type(container: QObject) -> int:
        """
        return: 0 for row, 1 for column.
        help: if container is row, it has property 'effectiveLayoutDirection'
            (the value is Qt.LeftToRight(=0) or Qt.RightToLeft(=1)), while
            column doesn't have this property(=None).
        """
        if container.property('effectiveLayoutDirection') is None:
            return 1
        else:
            return 0


pylayout = LayoutHelper()
