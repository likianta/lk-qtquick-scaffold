import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

Column {
    id: _root
    // anchors.fill: parent
    anchors.margins: LCGeometry.MarginM
    padding: 0
    spacing: LCGeometry.VSpacingM

    property bool p_alignCenter: true
    property bool p_fillWidth: true
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing
    // property alias p_topPadding: _root.topPadding; property alias p_bottomPadding: _root.bottomPadding
    property int p_vpadding: 0

    Component.onCompleted: {
        _root.topPadding = p_vpadding
        _root.bottomPadding = p_vpadding

        if (p_alignCenter) {
            for (let i in _root.children) {
                _root.children[i].anchors.horizontalCenter = _root.horizontalCenter
            }
        }

        if (p_fillWidth) {
            for (let i in _root.children) {
                _root.children[i].width = _root.width
            }
        }
    }
}
