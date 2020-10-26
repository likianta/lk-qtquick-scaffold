"""
@Author   : likianta (likianta@foxmail.com)
@FileName : layout_helper.py
@Version  : 0.1.0
@Created  : 2020-10-20
@Updated  : 2020-10-20
@Desc     : 帮助 QML 布局减少代码量, 使用封装好的函数实现批量化的属性操作 (替代
    部分 JavaScript 功能).
"""
from PySide2.QtCore import Slot
from PySide2.QtQml import QQmlProperty
from lk_logger import lk

from _typing import *
from launcher import Application


class LayoutHelper(QObject):
    """
    注意事项:
        锚点系统无法通过 LayoutHelper 设置. 例如, `Rectangle.left`, 它是一个
            QQuickAnchorLine 对象, 在 Python 中没有与之对应的转换器, 所以我们无
            法在 Python 中这样做:
                # 假设已知 parent 和 rect 是父子关系的两个 QObject.
                rect.setProperty('anchors.left', parent.left)
            报错信息: RuntimeError: Can't find converter for 'QQuickAnchorLine'.
    """
    
    def __init__(self, app: Application):
        super().__init__()
        app.register_pyobj('LayoutHelper', self)

    @staticmethod
    def _get_children(item: QObject) -> List[QObject]:
        """
        注意: `item.children()` 返回的列表中, 包含位置的 QObject.
            测试示例:
                // qml
                Rectangle {
                    id: _rect
                    Text {objectName: "t1"; text: "A"}
                    Text {objectName: "t2"; text: "B"}
                    Component.onCompleted: {
                        console.log(_rect.children.length)  # -> 2
                    }
                }
                
                # python
                children = rect.children()
                #   -> [QObject, QObject, QObject], 理应有两个, 却出现了三个
                names = [child.property('objectName') for child in children]
                #   -> ['t1', 't2', '']
            目前没有很好的方法区分并去除这个未知的 QObject, 现在利用的是
            'enabled' 属性来判断: 如果 `child.property('enabled')` 返回的是
            bool, 则认为是正常的 QObject; 如果是 None, 则认为是未知的 QObject.
        """
        return [child for child in item.children()
                if child.property('enabled') is not None]

    @Slot(QObj)
    def debug(self, item: QObject):
        from PySide2.QtQml import QQmlProperty
        parent = item.parent()
        x = QQmlProperty(item, 'anchors')
        y = QQmlProperty(parent, 'right')
        lk.loga(x.read())
        z = QQmlProperty(x.read(), 'right')
        lk.loga(z)
        z.write(y)

    @Slot(QObj, QVar)
    def set_children_props(self, parent: QObj, props: QJSValue):
        props = props.toVariant()  # type: dict
        for child in self._get_children(parent):
            for k, v in props.items():
                # child.setProperty(k, v)  # A
                prop = QQmlProperty(child, k)  # B
                prop.write(v)  # B
                #   NOTE: scheme B is more stable than A.

    '''
    def _emulate_anchors(self, qobj1, qobj2, align: str):  # FIXME or DELETE
        if '-' in align:
            i, j = align.split('-')
            return self._emulate_anchors(qobj1, qobj2, i) and \
                   self._emulate_anchors(qobj1, qobj2, j)

        qobj2_anchors = {
            'x'          : _x := qobj2.property('x'),
            'y'          : _y := qobj2.property('y'),
            'real_width' : _w := qobj2.property('width') -
                                 (qobj2.property['leftPadding'] or 0) -
                                 (qobj2.property['rightPadding'] or 0),
            'real_height': _h := qobj2.property('height') -
                                 (qobj2.property['topPadding'] or 0) -
                                 (qobj2.property['bottomPadding'] or 0),
            'center_x'   : (_x + _w / 2, _y + _h / 2)
        }

        if align == 'fill':
            qobj1.setProperty('x', qobj2_anchors['x'])
            qobj1.setProperty('y', qobj2_anchors['y'])
            qobj1.setProperty('width', qobj2_anchors['real_width'])
            qobj1.setProperty('height', qobj2_anchors['real_height'])
        elif align == 'center':
            pass
    '''
