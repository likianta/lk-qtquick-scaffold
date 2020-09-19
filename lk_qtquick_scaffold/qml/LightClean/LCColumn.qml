import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

Column {
    id: _root
    anchors.margins: LCGeometry.MarginM
    padding: 0
    spacing: LCGeometry.VSpacingM

    property bool p_alignCenter: true
    property bool p_fillWidth: true
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    Component.onCompleted: {
        if (p_alignCenter) {
            _root.children.forEach(x => {
                x.anchors.horizontalCenter = _root.horizontalCenter
            })
        }
        if (p_fillWidth) {
            _root.children.forEach(x => {
                x.width = _root.width
            })
        }
    }
}
