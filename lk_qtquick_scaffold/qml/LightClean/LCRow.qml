import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry

Row {
    id: _root
    anchors.leftMargin: LCGeometry.MarginM; anchors.rightMargin: LCGeometry.MarginM
    height: LCGeometry.BarHeight
    padding: 0
    spacing: LCGeometry.HSpacingM

    property bool p_alignCenter: false
    property bool p_fillHeight: true
    property int p_hpadding: 0
    // property alias p_leftPadding: _root.leftPadding; property alias p_rightPadding: _root.rightPadding
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing

    onHeightChanged: {
        // https://stackoverflow.com/questions/24577075/what-is-the-order-of-component-oncompleted-in-a-qml-file-with-many-items
        // Because of the undefined order of instantiating in
        //  `Component.onCompleted`, we cannot dicide `p_fillHeight` whether
        //  works as our expect. So we observe the height changing and update to
        //  make sure the children got exactly height-filled.
        if (p_fillHeight) {
            for (let i in _root.children) {
                _root.children[i].height = _root.height
                // console.log("LCRow", _root.height, _root.children[i].height)
            }
        }
    }

    Component.onCompleted: {
        _root.leftPadding = p_hpadding
        _root.rightPadding = p_hpadding
    
        if (p_alignCenter) {
            for (let i in _root.children) {
                _root.children[i].anchors.verticalCenter = _root.verticalCenter
            }
        }
    }
}
