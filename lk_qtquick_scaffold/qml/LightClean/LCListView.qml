import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

ListView {
    id: _root
    // anchors.margins: LCGeometry.MarginM
    clip: true
    model: p_model
    spacing: LCGeometry.VSpacingXS

    property alias p_currentIndex: _root.currentIndex
    property alias p_delegate: _root.delegate
    property var p_model: Array()  // <[str, ...], [dict, ...]>
    property alias p_spacing: _root.spacing
    property int r_count: p_model.length
    property alias r_currentItem: _root.currentItem

    Component.onCompleted: {
        if (_root.height == 0) {
            _root.height = childrenRect.height
        }
    }
}