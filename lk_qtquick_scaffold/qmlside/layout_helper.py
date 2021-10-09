from PySide6.QtCore import QObject
from PySide6.QtCore import Slot
from PySide6.QtQml import QmlElement
from PySide6.QtQml import QJSEngine

from ..typehint import *


QML_IMPORT_NAME = "lk_qtquick_scaffold.qmlside.layout_helper"
QML_IMPORT_MAJOR_VERSION = 1

qjs_engine = QJSEngine()


@QmlElement
class LKLayoutHelper(QObject):
    
    @Slot(QObject)
    def halign_children(self, parent: QObject, padding, spacing):
        width = parent.property('width') - padding * 2 - spacing * (len(parent.children()) - 1)
        
        children = parent.children()
        
        
        
        for i in parent.children():
            i = ''
    
