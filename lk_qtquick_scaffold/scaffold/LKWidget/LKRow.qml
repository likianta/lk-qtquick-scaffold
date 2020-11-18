import QtQuick 2.15
import "./LKStyle/dimension.js" as LKGeometry

Row {
    id: _root
    anchors.leftMargin: LKGeometry.MarginM; anchors.rightMargin: LKGeometry.MarginM
    anchors.margins: 0
    height: LKGeometry.BarHeight
    spacing: LKGeometry.HSpacingM

    property bool p_alignCenter: true
    property bool p_fillEnd: false
    property bool p_fillHeight: true
    // property int p_hpadding: 0
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    Component.onCompleted: {
        if (p_fillHeight) {
            for (let i in _root.children) {
                _root.children[i].height = _root.height
                // console.log("LKRow", _root.height, _root.children[i].height)
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
