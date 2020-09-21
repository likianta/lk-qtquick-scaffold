import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

Row {
    id: _root
    anchors.leftMargin: LCGeometry.MarginM; anchors.rightMargin: LCGeometry.MarginM
    anchors.margins: 0
    height: LCGeometry.BarHeight
    spacing: LCGeometry.HSpacingM

    property bool p_alignCenter: false
    property bool p_fillEnd: false
    property bool p_fillHeight: true
    // property int p_hpadding: 0
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    Component.onCompleted: {
        if (p_fillHeight) {
            for (let i in _root.children) {
                _root.children[i].height = _root.height
                // console.log("LCRow", _root.height, _root.children[i].height)
            }
        }
        if (p_fillEnd) {
            const lastChild = _root.children[_root.children.length - 1]
            lastChild.width = _root.width - lastChild.x - _root.anchors.margins
        }
        if (p_alignCenter) {
            for (let i in _root.children) {
                _root.children[i].anchors.verticalCenter = _root.verticalCenter
            }
        }
    }
}
