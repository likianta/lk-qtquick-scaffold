"""
@Author   : likianta (likianta@foxmail.com)
@FileName : pycomm.py
@Version  : 0.6.0
@Created  : 2020-09-09
@Updated  : 2020-09-24
@Desc     : 
"""

from PySide2.QtCore import QAbstractListModel, QMetaObject, Qt, Slot
from lk_logger import lk

from _typing import *


# noinspection PyUnresolvedReferences
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
        self._datapot = {}  # type: Dict[str, Tuple[QVal, QSource]]
        self._hooks = set()  # type: Set[QObj]
        self._qobj_holder = {}  # type: Dict[QPath, Dict[QUid, QObj]]
        #   {path: {uid: obj}}
        #   e.g. {'./ui/SomeComp.qml': {'_txt': PySide2.QtCore.QObject}}
    
    @Slot(QObj)
    def scanning_qml_tree(self, root: QObj):
        """
        使用方法:
            示例: 在 QML 根布局中 (通常是 Window), 调用:
                    Window {
                        id: _root
                        ...
                        Component.onCompleted: {
                            PyHooks.scanning_qml_tree(_root)
                        }
                    }
                PyHooks 将从根布局出发, 遍历所有子对象, 如果子对象中包含以下属性:
                    Item {
                        property var pyhook
                        ...
                    }
                则该对象的 pyhook 会经过解析, 更新到 PyHooks._hooks 字典中.
            语法格式定义:
                `property var pyhook` 支持以下格式:
                    1. property var pyhook: {key: val, ...}
                        key 可以自定义, 但需保证全局唯一.
                        val 可以是常见的 js 类型 (基本类型, list, dict), 也可以
                            是指该组件的某个已存在的属性值, 比如 Button 的 text,
                            width, height, x, y, background 等, 注意:
                            1. 当作属性时, 格式为 ':width' (以冒号开头的字符串).
                            2. 属性 id 不能用作 val, 即 ':id' 会导致程序有报错的
                                风险.
                        示例: Button {
                            property var pyhook: {
                                'description': 'the main button',
                                'btn_name': ':text',
                            }
                        }
                    2. property var pyhook: [str key, str prop]
                        key 可以自定义, 但需保证全局唯一.
                        prop 指该组件的某个已存在的属性值, 比如 Button 的 text,
                        width, height, x, y, background 等, 注意 id 不能使用.
                        示例: Button {property var pyhook: ['event', 'text']}
                    3. property var pyhook: [[str key, str prop], ...]
                       示例: Button {
                            property var pyhook: [
                                ['btn_width', ':width'],
                                ['btn_height', ':height'],
                            ]
                        }
        注意:
            1. 在静态组件中设置 pyhook
            3. LCWindow 根布局不能设置 pyhook
            4. Repeater, ListView 等的 children 不能设置 pyhook. 如 children 需要
                更新 pyhook, 请调用 parent 的 pyhook
        """
        self._hooks.clear()
        
        def _search_pyhooks(node: QObj):
            for child_node in node.children():
                # lk.loga(child_node, child_node.property('pyhook'))
                if child_node.property('pyhook'):
                    self._hooks.add(child_node)
                else:  # None
                    _search_pyhooks(child_node)
        
        _search_pyhooks(root)
        lk.loga(len(self._hooks))
    
    def _unpack_hooks(self):
        def _unpack_kv():
            if isinstance(v, str) and v.startswith(':'):
                # e.g. k = 'btn_name', v = ':text'
                #   -> yield 'btn_name', item.property('text')
                yield k, item.property(v[1:])
            else:
                # e.g. k = 'btn_width', v = 80
                #   -> yield 'btn_width', 80
                yield k, v
        
        for item in self._hooks:
            kv = item.property('pyhook').toVariant()
            """ |dict|list|double_list|
                dict: {key: val, ...}
                    key: str
                    val: |str|int|bool|list|dict|None|
                        str: 1. str startswith ':' like ':text', it aims to
                                item's existed property.
                             2. str not startswith ':', it just a plain string.
                list: [key, val]
                double_list: [[key1, val1], [key2, val2], ...]
            """
            if isinstance(kv, dict):
                for k, v in kv.items():
                    yield from _unpack_kv()
            else:
                if isinstance(kv[0], str):
                    k, v = kv
                    yield from _unpack_kv()
                else:
                    for (k, v) in kv:
                        yield from _unpack_kv()
    
    def get_qparams(self):
        return {k: v for k, v in self._unpack_hooks()}
    
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
        self._datapot[key] = (val.toVariant(), source)
    
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
        return self._datapot.get(key, [None, ''])[0]
    
    # --------------------------------------------------------------------------
    
    @Slot()
    @Slot(str)
    @Slot(str, str)
    def debug(self, source='', view='_qobj_holder'):
        lk.loga(source, view)
        lk.init_count()
        if view == '_qobj_holder':
            if self._qobj_holder:
                for path, val in self._qobj_holder.items():
                    for uid, obj in val.items():
                        lk.logax(path, uid, obj)
            else:
                lk.loga(self._qobj_holder)
        elif view == '_datapot':
            for k, v in self._datapot.items():
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
        node = self._qobj_holder.setdefault(path, {})
        node[uid] = obj
    
    @Slot(str, QVal)
    def set_dict(self, path: str, uid2obj: QVal):
        node = self._qobj_holder.setdefault(path, {})
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
            return self._qobj_holder[path][uid]
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
        return list(self._qobj_holder[path].values())
    
    @Slot(str, result=QVar)
    def get_dict(self, path) -> Dict[QUid, QObj]:
        return self._qobj_holder[path]
    
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
        lk.loga(func.__name__, h='parent')
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
