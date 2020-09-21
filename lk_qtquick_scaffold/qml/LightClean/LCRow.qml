import QtQuick 2.14
import QtQuick.Layouts 1.14
import "./LCStyle/geometry.js" as LCGeometry

RowLayout {
    id: _root
    // anchors.leftMargin: LCGeometry.MarginM; anchors.rightMargin: LCGeometry.MarginM
    anchors.margins: LCGeometry.MarginM
    height: LCGeometry.BarHeight
    spacing: LCGeometry.HSpacingM

    property bool p_fillHeight: true
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    Component.onCompleted: {
        if (p_fillHeight) {
            for (let i in _root.children) {
                _root.children[i].height = _root.height
                // if (_root.children[i].height == 0) {
                //     _root.children[i].Layout.fillHeight = true
                // }
            }
        }
    }
}
