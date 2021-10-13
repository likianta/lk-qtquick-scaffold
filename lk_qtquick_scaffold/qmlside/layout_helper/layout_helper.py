from PySide6.QtCore import QObject

from .anchors import Anchors
from .container_alignment import ContainerAlignment
from .content_alignment import ContentAlignment


class LayoutHelper(QObject, Anchors, ContainerAlignment, ContentAlignment):
    pass
