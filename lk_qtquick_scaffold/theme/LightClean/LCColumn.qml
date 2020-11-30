import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension
import "../../qml_helper/layout_helper.js" as LCLayout

Column {
    id: root
    padding: LCDimension.Padding
    spacing: LCDimension.VSpacingM

    property bool  p_alignCenter: false  // whether children aligned to
    //      horizontal center
    property bool  p_autoHeight: true
    // property bool  p_fillRest: false  // fill the last item to the remaining
    //      space
    //      https://stackoverflow.com/questions/27319985/how-to-make-last-item
    //      -in-qml-container-fill-remaining-space
    property bool  p_fillWidth: false
    property alias p_padding: root.padding
    property alias p_spacing: root.spacing
    
    Component.onCompleted: {
        if (p_fillWidth) {
            for (let i in root.children) {
                root.children[i].width = root.width
            }
        }
        if (p_autoHeight) {
            LCLayout.autoHeight(root)
        }
        if (p_alignCenter) {
            for (let i in root.children) {
                root.children[i].anchors.horizontalCenter = root.horizontalCenter
            }
        }
    }
}
