from PySide6.QtCore import Property
from PySide6.QtCore import QObject

from ._patch import get_children
from ...pyside import slot


# TODO
# from .anchors import Anchors
# from .container_alignment import ContainerAlignment
# from .content_alignment import ContentAlignment


class Enum:
    HORIZONTAL = 0
    VERTICAL = 1
    STRETCH = -1
    SHRINK = -2


# class LayoutHelper(QObject, Anchors, ContainerAlignment, ContentAlignment):
class LayoutHelper(QObject):
    HORIZONTAL = Property(int, lambda _: 0, constant=True, final=True)
    VERTICAL = Property(int, lambda _: 1, constant=True, final=True)
    
    @slot(QObject, int)
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
    
    @slot(object, result=tuple)
    @slot(object, int, result=tuple)
    @slot(object, int, int, result=tuple)
    def calc_text_block_size(
            self, lines: list[str],
            char_width=10, line_height=20
    ):
        lines = tuple(map(str, lines))
        # OPTM: use different char_width for non-ascii characters.
        width = max(map(len, lines)) * char_width
        height = (len(lines) + 1) * line_height
        return width, height


pylayout = LayoutHelper()
