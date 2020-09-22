import QtQuick 2.14
import QtQml.Models 2.14
import "./LCStyle/geometry.js" as LCGeometry

Item {
    id: _root

    ListModel {
        id: _model
    }

    ListView {
        id: _list
        anchors.fill: parent
        anchors.margins: LCGeometry.MarginM
        clip: true
        model: _model
        spacing: LCGeometry.VSpacingXS
    }

    property bool p_autoSize: false  // DEL
    property alias p_currentIndex: _list.currentIndex
    property alias p_delegate: _list.delegate
    property int p_maxHeight: 0
    property alias p_spacing: _list.spacing
    property alias r_count: _model.count
    property alias r_currentItem: _list.currentItem

    function fn_getCurrent() {
        return [
            _list.currentIndex,
            _list.currentItem,
            _model.get(_list.currentIndex)
        ]
    }

    function fn_getCurrentIndex() {
        return _list.currentIndex
    }

    function fn_getCurrentItem() {
        return _list.currentItem
    }

    function fn_getCurrentModel() {
        return _model.get(_list.currentIndex)
    }

    function fn_findItem(index) {
        // https://forum.qt.io/topic/80573/qt-quick-listview-access-to-delegate-item+&cd=1&hl=zh-CN&ct=clnk&gl=sg
        if (index < _model.count) {
            _list.currentIndex = index
            return _list.currentItem
        } else {
            return null
        }
    }

    function fn_findData(index) {
        return _model.get(index)
    }

    function fn_clear() {
        _model.clear()
    }

    function fn_append(data) {
        _model.append(data)
    }

    function fn_addList(data) {
        for (var i in data) {
            // console.log("LCListModel", data[i])
            if (data[i] instanceof Object) {
                _model.append(data[i])
            } else {
                _model.append({"value": data[i]})
            }
        }

        if (p_autoSize) {
            let height = _model.count * 20
            if (p_maxHeight > 0) {
                height = height > p_maxHeight ? p_maxHeight : height
            }
            _root.height = height
        }
    }

    Component.onCompleted: {
        _root.height = _root.childrenRect.height + 100
    }
}