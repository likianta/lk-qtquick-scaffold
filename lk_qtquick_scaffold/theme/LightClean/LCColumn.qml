import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension

Column {
    id: _root
    anchors.margins: LCDimension.MarginM
    spacing: LCDimension.VSpacingM

    property bool  p_alignCenter: false
    property bool  p_fillEnd: false  // auto make the last item fill the remaining space.
    //  https://stackoverflow.com/questions/27319985/how-to-make-last-item-in-qml-container-fill-remaining-space
    property bool  p_fillWidth: true
    property alias p_margins: _root.anchors.margins
    property alias p_spacing: _root.spacing
    // property int p_vpadding: 0

    Component.onCompleted: {
        // _root.topPadding = p_vpadding
        // _root.bottomPadding = p_vpadding

        if (p_fillWidth) {
            for (let i in _root.children) {
                // console.log("LCColumn", _root, _root.width, _root.children[i].width)
                _root.children[i].width = _root.width
            }
        }
        if (p_fillEnd) {
            const lastChild = _root.children[_root.children.length - 1]
            lastChild.height = _root.height - lastChild.y - _root.anchors.margins
        }
        if (p_alignCenter) {
            for (let i in _root.children) {
                _root.children[i].anchors.horizontalCenter = _root.horizontalCenter
            }
        }
    }
}
