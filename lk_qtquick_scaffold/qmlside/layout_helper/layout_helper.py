from PySide6.QtCore import QObject
from PySide6.QtCore import Slot
from PySide6.QtQml import QJSValue

from .anchors import Anchors
from .container_alignment import ContainerAlignment
from .content_alignment import ContentAlignment
from .type_adapter import adapt_argtypes


class LayoutHelper(QObject, Anchors, ContainerAlignment, ContentAlignment):
    
    # noinspection PyTypeChecker
    @Slot(QJSValue, result=list)
    @Slot(QJSValue, int, result=list)
    @Slot(QJSValue, int, int, result=list)
    @adapt_argtypes
    def calc_model_size(self, model: list, char_width=10, line_height=20):
        model = tuple(map(str, model))
        # OPTM: use different char_width for non-ascii characters.
        width = max(map(len, model)) * char_width
        height = (len(model) + 1) * line_height
        return width, height


pylayout = LayoutHelper()
