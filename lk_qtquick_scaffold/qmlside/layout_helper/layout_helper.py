from PySide6.QtCore import QObject
from PySide6.QtCore import Slot

from ._ext import TQVal
from ._ext import adapt_argtypes
from .anchors import Anchors
from .container_alignment import ContainerAlignment
from .content_alignment import ContentAlignment


class LayoutHelper(QObject, Anchors, ContainerAlignment, ContentAlignment):
    
    # noinspection PyTypeChecker
    @Slot(TQVal, result=list)
    @Slot(TQVal, int, result=list)
    @Slot(TQVal, int, int, result=list)
    @adapt_argtypes
    def calc_model_size(self, model: list, char_width=10, line_height=20):
        model = tuple(map(str, model))
        # OPTM: use different char_width for non-ascii characters.
        width = max(map(len, model)) * char_width
        height = (len(model) + 1) * line_height
        return width, height
