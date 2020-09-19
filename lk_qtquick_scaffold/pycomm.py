"""
@Author   : likianta (likianta@foxmail.com)
@FileName : pycomm.py
@Version  : 0.4.3
@Created  : 2020-09-09
@Updated  : 2020-09-19
@Desc     : 
"""

from PySide2.QtCore import QAbstractListModel, QMetaObject, Qt, Slot
from lk_logger import lk

from _typing import *


class PyHooks(QObject):
    """ Hookup qml objects, and store the reference in Python dict.
    
    The Concept:
        uid: an uid is unique under the same path. e.g. '_mouse_area'.
        obj: QObject (qml component object).
        path: e.g. './ui/SomeFolder/SomeComp.qml'.
        url: consists of `{path}#{uid}`. e.g. './ui/SomeFolder/SomeComp.qml#
            _mouse_area'.
    """
    
    def __init__(self):
        super().__init__()
        self.hooks = {}  # type: Dict[QPath, Dict[QUid, QObj]]
        #   {path: {uid: obj}}
        #   e.g. {'./ui/SomeComp.qml': {'_txt': PySide2.QtCore.QObject}}
        self.values = {}  # type: Dict[str, Tuple[QVal, QSource]]
    
    @Slot(str, QVal, str)
    @Slot(str, QVal)
    def set_value(self, key: str, val: QVal, source=''):
        """
        Usecase (in .qml file):
            // === view.qml ===
            Item {
                id: _item
                Component.onCompleted: {
                    // a.
                    PyHooks.set_value("week", "Wednesday", "view.qml#_item")
                    // b.
                    PyHooks.set_value("week", "Wednesday")
                }
            }
        
        :param key:
        :param val:
        :param source:
        :return:
        """
        self.values[key] = (val.toVariant(), source)
    
    @Slot(str, result=QVar)
    def get_value(self, key: str) -> Any:
        """
        Usecase (in .qml file):
            Item {
                Component.onCompleted: {
                    let data = PyHooks.get_value("week")  # -> "Wednesday"
                }
            }
        
        :param key:
        :return:
        """
        return self.values.get(key, [None, ''])[0]
    
    # --------------------------------------------------------------------------
    
    @Slot()
    @Slot(str)
    @Slot(str, str)
    def debug(self, source='', view='hooks'):
        lk.loga(source, view)
        lk.init_count()
        if view == 'hooks':
            if self.hooks:
                for path, val in self.hooks.items():
                    for uid, obj in val.items():
                        lk.logax(path, uid, obj)
            else:
                lk.loga(self.hooks)
        elif view == 'values':
            for k, v in self.values.items():
                lk.logax(k, v)
    
    @staticmethod
    def _qjsval_2_pylist(qids):  # DELETE
        """
        调用方可能有以下两种传递方式:
            // === SomeComp.qml ===
            import QtQuick 2.15
            Rectangle {
                Component.onCompleted: {
                    // 方式 1: 请求一个字符串.
                    var hooks1 = PyHooks.get_hooks("ABC")
                    # -> {ABC: Object}

                    // 方式 2: 请求一个字符串列表.
                    var hooks2 = PyHooks.get_hooks(["ABC", "DEF"])
                    # -> {ABC: Object1, DEF: Object2}
                }
            }
        :param qids:
        :return:
        """
        qids = qids.toVariant()  # type: list
        # qids.toVariant() 可能是一个列表 (方式 2), 也可能是一个字符串 (方式 1),
        #   我们得把后者转换成单元素的列表/元组.
        if isinstance(qids, str):
            # noinspection PyTypeChecker
            qids = (qids,)
        # lk.loga(qids)
        return qids
    
    # --------------------------------------------------------------------------
    
    @Slot(str, QObj)
    def set_one(self, url: str, obj: QObj):
        path, uid = url.rsplit('#', 1)
        node = self.hooks.setdefault(path, {})
        node[uid] = obj
    
    @Slot(str, QVal)
    def set_dict(self, path: str, uid2obj: QVal):
        node = self.hooks.setdefault(path, {})
        uid2obj = uid2obj.toVariant()  # type: dict
        node.update(uid2obj)
    
    @Slot(QVal)
    @Slot(str, QVal)
    @Slot(str, QObj)
    def set(self, unknown1: Union[QPath, QUrl, QVal],
            unknown2: Union[QObj, QVal] = None):
        """ Set one object or set dict of objects.

        :param unknown1:
            QPath, QUrl: depends on obj (if obj is QObj, unknown is url, if obj
                is dict of objects, unknown is path).
            QVal: {url: obj} (in this case obj param must be None).
        :param unknown2
            QObj: one object. -> obj
            QVal: one dict of objects. -> {uid: obj}
        """
        if isinstance(unknown1, str):
            if isinstance(unknown2, QObj):  # set one.
                url, obj = unknown1, unknown2
                self.set_one(url, obj)
            else:  # set dict. the unknown2 is `uid2obj` (dict).
                path, uid2obj = unknown1, unknown2
                # noinspection PyTypeChecker
                self.set_dict(path, uid2obj)
        else:
            assert unknown2 is None
            urls2obj = unknown1.toVariant()  # type: dict
            for url, unknown2 in urls2obj.items():
                self.set_one(url, unknown2)
    
    # --------------------------------------------------------------------------
    
    # noinspection PyTypeChecker
    @Slot(str, result=QObj)
    def get_one(self, url: QUrl) -> Union[QObj, None]:
        path, uid = url.rsplit('#', 1)
        try:
            return self.hooks[path][uid]
        except KeyError as e:
            lk.logt('[W2116]', 'Cannot find key', e)
            return None
    
    @Slot(str, result=QVar)
    def get_list(self, path) -> List[QObj]:
        """
        NOTE: This method is not often to use.
        :param path:
        :return:
        """
        return list(self.hooks[path].values())
    
    @Slot(str, result=QVar)
    def get_dict(self, path) -> Dict[QUid, QObj]:
        return self.hooks[path]
    
    @Slot(str, result=QVar)
    @Slot(QVal, result=QVar)
    def get(self, unknown: Union[QUrl, QPath, QVal]) \
            -> Union[QObj, List[QObj], Dict[QUid, QObj], None]:
        """
        Usecase:
            PyHooks.get("./ui/SomeComp.qml") -> {'_txt': obj, ...}
            PyHooks.get("./ui/SomeComp.qml#_txt") -> obj
            PyHooks.get([
                "./ui/SomeComp.qml#_txt",
                "./ui/AnotherComp.qml#_txt",
            ]) -> [obj1, obj2]

        :param unknown:
            a. str path -> return {uid: obj, ...} (uid from same path)
            b. str url -> return single obj
            c. list urls -> return [obj, ...] (obj from different paths)
        :return:
        """
        if isinstance(unknown, str):
            if '#' in unknown:
                url = unknown
                return self.get_one(url)
            else:
                path = unknown
                return self.get_dict(path)
        else:
            urls = unknown.toVariant()  # type: list
            return list(map(self.get_one, urls))


class QtHooks(QObject):
    
    def __init__(self, engine, pyhooks: PyHooks):
        super().__init__()
        self._engine = engine
        self._pyhooks = pyhooks
    
    def get(self, uid: QUid):
        return self._pyhooks.get(uid)
    
    find = get
    
    def update(self, uid: QUid, prop: str, value: Any):
        qobj = self.get(uid)  # type: QObj
        qobj.setProperty(prop, value)
    
    # noinspection PyTypeChecker
    def update_list_model(self, uid: QUid, *values: dict, clear=False,
                          birdge_data='py_newData', bridge_method='pyAppend'):
        qobj = self.get(uid)  # type: QAbstractListModel
        if clear:
            QMetaObject.invokeMethod(qobj, 'clear', Qt.AutoConnection)
        for v in values:
            qobj.setProperty(birdge_data, v)
            QMetaObject.invokeMethod(qobj, bridge_method, Qt.AutoConnection)
    
    # noinspection PyTypeChecker
    def invoke_qml(self, uid: QUid, method: str):
        """ Invoke QML method.
        仅支持调用无参方法.
        """
        qobj = self.get(uid)
        QMetaObject.invokeMethod(qobj, method, Qt.AutoConnection)
    
    # --------------------------------------------------------------------------
    
    __msg_box = {}
    
    @Slot(QUid)
    @Slot(QUid, str)
    def put_in_msg(self, uid, msg=''):
        self.__msg_box[uid] = msg
        return uid, msg
    
    # TODO
    # def recv(self, *uids, timeout=None):
    #     # from asyncio import sleep, get_event_loop, wait
    #     def listen(_uids):
    #         lk.logax(_uids)
    #
    #         elapsed_time = 0.0
    #
    #         # while True:
    #         for uid in _uids:
    #             if uid in self.__msg_box:
    #                 self.__msg_box.clear()
    #                 return uid, self.__msg_box[uid]
    #
    #         elapsed_time += 0.5
    #         if timeout is not None and elapsed_time > timeout:
    #             self.__msg_box.clear()
    #             return '', ''
    #
    #         self.__msg_box.clear()
    #         return '', ''


class PyHandler(QObject):
    
    def __init__(self):
        super().__init__()
        self.__pymethods_dict = {}
    
    @Slot(str, QVal, result=QVar)
    @Slot(str, result=QVar)
    def main(self, method: str, params: QVal = None):
        try:
            if params is None:
                return self.__pymethods_dict.get(
                    method, self._invalid_method)()
            else:
                # noinspection PyArgumentList
                return self.__pymethods_dict.get(
                    method, self._invalid_method)(params.toVariant())
        except Exception as e:
            raise Exception('PyHandler executing error', e)
    
    def register_pymethod(self, func: staticmethod):
        """
        https://medium.com/%40mgarod/dynamically-add-a-method-to-a-class-in
            -python-c49204b85bd6+&cd=3&hl=zh-CN&ct=clnk&gl=sg
        """
        lk.loga(func.__name__)
        self.__pymethods_dict[func.__name__] = func  # A
        # setattr(self, func.__name__, func)  # B
    
    def _invalid_method(self, *args):
        return
    
    @staticmethod
    def find_pyhandler_related_methods(qmldir: str, base: str):
        from lk_utils.filesniff import findall_files, path_on_rel
        from lk_utils.read_and_write import read_file_by_line
        
        for filepath in findall_files(qmldir, suffix='.qml'):
            for i, x in enumerate(read_file_by_line(filepath, 1)):
                if (x := x.strip()).startswith('//'):
                    continue
                if 'PyHandler.main' in x:
                    relpath = path_on_rel(filepath, base)
                    print(f'{relpath}:{i}', '>>', x)
