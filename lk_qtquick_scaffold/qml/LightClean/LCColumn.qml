import QtQuick 2.14
import QtQuick.Layouts 1.14
import "./LCStyle/geometry.js" as LCGeometry

ColumnLayout {
    id: _root
    // anchors.leftMargin: LCGeometry.MarginM; anchors.rightMargin: LCGeometry.MarginM
    anchors.margins: LCGeometry.MarginM
    width: LCGeometry.BarWidth
    spacing: LCGeometry.HSpacingM

    property bool p_fillWidth: true
    property int p_hmargins: 0
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    Component.onCompleted: {
        if (p_hmargins > 0) {
            _root.anchors.leftMargin = p_hmargins
            _root.anchors.rightMargin = p_hmargins
        }
        if (p_fillWidth) {
            for (let i in _root.children) {
                _root.children[i].Layout.fillWidth = true
            }
        }
    }
}
