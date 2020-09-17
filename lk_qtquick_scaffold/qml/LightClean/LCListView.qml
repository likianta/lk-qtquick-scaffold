import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

Item {
    id: _root

    property alias p_delegate: _list.delegate
    property alias p_spacing: _list.spacing
    property bool p_autoSize: false
    property int p_maxHeight: 0

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
            let height = _model.count * 20
            if (p_maxHeight > 0) {
                height = height > p_maxHeight ? p_maxHeight : height
            }
            _root.height = height
        }
    }

    LCListModel {
        id: _model
    }

    ListView {
        id: _list
        anchors.fill: parent
        anchors.margins: LCGeometry.MarginM
        clip: true
        model: _model
        spacing: LCGeometry.SpacingM.VSpacingS
    }

    Component.onCompleted: {
        _root.height = _root.childrenRect.height + 100
    }
}