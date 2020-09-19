import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

Row {
    id: _root
    anchors.leftMargin: LCGeometry.MarginM; anchors.rightMargin: LCGeometry.MarginM
    height: LCGeometry.BarHeight
    padding: 0
    spacing: LCGeometry.HSpacingM

    property bool p_alignCenter: true
    property bool p_fillHeight: true
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing
    property alias p_topPadding: _root.topPadding; property alias p_bottomPadding: _root.bottomPadding

    Component.onCompleted: {
        if (p_alignCenter) {
            _root.children.forEach(x => {
                x.anchors.horizontalCenter = _root.horizontalCenter
            })
        }
        if (p_fillHeight) {
            _root.children.forEach(x => {
                x.height = _root.height
            })
        }
    }
}
