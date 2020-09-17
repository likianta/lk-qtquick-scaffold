import QtQuick 2.14

Item {
    id: _root
    // property alias obj_ListView: _list
    property alias p_delegate: _list.delegate
    property bool p_autoSize: false
    property int p_maxHeight: 100

    function fn_clear() {
        _model.clear()
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
            const height = _model.count * 20
            _root.height = height > p_maxHeight ? p_maxHeight : height
        }
    }

    LCListModel {
        id: _model
    }

    ListView {
        id: _list
        anchors.fill: parent
        model: _model
    }

    Component.onCompleted: {
        _root.height = _root.childrenRect.height + 100
    }
}