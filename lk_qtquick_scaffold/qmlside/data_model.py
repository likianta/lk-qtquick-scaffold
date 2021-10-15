from PySide2.QtGui import Qt
from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QObject
from PySide6.QtCore import Slot

from ._ext import Any
from ._ext import TQVal
from ._ext import TQVar
from .type_adapter import adapt_argtypes


class Model(QAbstractListModel):
    """
    https://pyblish.gitbooks.io/developer-guide/content/qml_and_python
    _interoperability.html
    https://stackoverflow.com/questions/54687953/declaring-a-qabstractlistmodel
    -as-a-property-in-pyside2
    """
    role_names: dict[int, bytes]
    items: list[dict[bytes, Any]]
    
    def __init__(self, role_names: list[str]):
        super().__init__()
        self.role_names = {
            i: n.encode(encoding='utf-8')
            for i, n in enumerate(role_names, Qt.UserRole + 1)
        }
        self.items = []
    
    def append(self, item: dict):
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount()
        )
        self.items.append({k.encode(encoding='utf-8'): v
                           for k, v in item.items()})
        self.endInsertRows()
    
    # noinspection PyMethodOverriding
    def data(self, index, role: int):
        # if role not in self.role_names:
        #     return ''
        
        name = self.role_names[role]
        # lk.loga(index, index.row(), role, name,
        #         self.items[index.row()].get(name, ''))
        return self.items[index.row()].get(name, '')
    
    # noinspection PyMethodOverriding,PyTypeChecker,PyUnresolvedReferences
    def setData(self, index, value, role):
        name = self.role_names[role]
        self.items[index.row()][name] = value
        self.dataChanged.emit(index, index)
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.items)
    
    def roleNames(self):
        # lk.logt('[D5645]', self.role_names)
        return self.role_names


class ModelGenerator(QObject):
    """
    QML Usages:
        ListView {
            model: LKModelGenerator.create([
                { name: 'aaa', age: 22 },
                { name: 'bbb', age: 33 },
                ...
            ])
        }
        
        ListView {
            model: LKModelGenerator.create(
                ['name', 'age'], // explicitly define the roles.
                [
                    { name: 'aaa' },
                    //  if we have explicitly defined the roles, we can write
                    //  incomplete values here. but be notice that the missing
                    //  value will be given str type.
                    { name: 'bbb', age: 33 },
                    ...
                ]
            )
        }
    """
    
    @Slot(TQVal, result=TQVar)
    @Slot(TQVal, TQVal, result=TQVar)
    @adapt_argtypes
    def create(self, a, b=None):
        if b is None:
            if isinstance(a, dict):
                a = [a]
            names = list(a[0].keys())
            data = a
        else:
            if isinstance(b, dict):
                b = [b]
            names = a
            data = b
        
        model = Model(names)
        for item in data:
            model.append(item)
        _holder.append(model)
        return model


_holder = []
