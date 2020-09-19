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
    property int p_hpadding: 0
    // property alias p_leftPadding: _root.leftPadding; property alias p_rightPadding: _root.rightPadding
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    Component.onCompleted: {
        _root.leftPadding = p_hpadding
        _root.rightPadding = p_hpadding
    
        if (p_alignCenter) {
            for (let i in _root.children) {
                _root.children[i].anchors.verticalCenter = _root.verticalCenter
            }
        }
        
        if (p_fillHeight) {
            for (let i in _root.children) {
                _root.children[i].height = _root.height
            }
        }
    }
}
