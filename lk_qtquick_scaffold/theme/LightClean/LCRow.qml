import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension
import "../qml_helper/layout_helper.js" as LCLayout

Row {
    id: root
    height: LCDimension.BarHeight
    padding: LCDimension.Padding
    spacing: LCDimension.HSpacingM

    property bool  p_alignCenter: true
    property bool  p_autoWidth: true
    property bool  p_fillHeight: true
    property alias p_margins: root.anchors.margins
    property alias p_padding: root.padding
    property alias p_spacing: root.spacing

    Component.onCompleted: {
        if (p_fillHeight) {
            root.children.forEach(x => {
                x.height = root.height
            })
            // for (let i in root.children) {
            //     root.children[i].height = root.height
            //     // console.log("LCRow", root.height, root.children[i].height)
            // }
        }
        if (p_autoWidth) {
            LCLayout.autoWidth(root)
        }
        if (p_alignCenter) {
            root.children.forEach(x => {
                x.anchors.verticalCenter = root.verticalCenter
            })
            // for (let i in root.children) {
            //     root.children[i].anchors.verticalCenter = root.verticalCenter
            // }
        }
    }
}
