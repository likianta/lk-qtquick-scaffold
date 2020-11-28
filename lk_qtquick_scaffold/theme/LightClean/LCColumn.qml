import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension

Column {
    id: root
    anchors.margins: LCDimension.MarginM
    spacing: LCDimension.VSpacingM

    property bool  p_alignCenter: false  // whether children aligned to horizontal center
    property bool  p_fillRest: false  // fill the last item to the remaining space
    //      https://stackoverflow.com/questions/27319985/how-to-make-last-item-in-qml-container-fill-remaining-space
    property bool  p_fillWidth: true
    property alias p_margins: root.anchors.margins
    property alias p_spacing: root.spacing
    
    Component.onCompleted: {
        // root.topPadding = p_vpadding
        // root.bottomPadding = p_vpadding

        if (p_fillWidth) {
            for (let i in root.children) {
                root.children[i].width = root.width
            }
        }
        if (p_fillRest) {
            const lastChild = root.children[root.children.length - 1]
            lastChild.height = root.height - lastChild.y - root.anchors.margins
        }
        if (p_alignCenter) {
            for (let i in root.children) {
                root.children[i].anchors.horizontalCenter = root.horizontalCenter
            }
        }
    }
}
