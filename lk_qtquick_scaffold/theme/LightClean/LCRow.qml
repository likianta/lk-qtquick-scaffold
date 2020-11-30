import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension
import "../../qml_helper/layout_helper.js" as LCLayout

Row {
    id: root
    // implicitWidth: LCDimension.BarWidth
    // implicitHeight: LCDimension.BarHeight
    width: LCDimension.BarWidth
    height: LCDimension.BarHeight
    padding: LCDimension.Padding
    spacing: LCDimension.HSpacingM

    property bool  p_alignCenter: true
    property bool  p_autoWidth: true
    property bool  p_fillHeight: false
    property alias p_padding: root.padding
    property alias p_spacing: root.spacing

    Component.onCompleted: {
        if (p_fillHeight) {
            for (let i in root.children) {
                root.children[i].height = root.height
            }
        }
        if (p_autoWidth) {
            LCLayout.autoWidth(root)
        }
        if (p_alignCenter) {
            for (let i in root.children) {
                root.children[i].anchors.verticalCenter = root.verticalCenter
            }
        }

        // console.log('LCRow:32', root.x, root.y, root.width, root.height)
        // for (let i in root.children) {
        //     const x = root.children[i]
        //     console.log('LCRow:35', x.x, x.y, x.width, x.height)
        // }
    }
}
