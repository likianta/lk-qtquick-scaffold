import QtQuick 2.15
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo
import "../../qml_helper/layout_helper.js" as LCLayout

Text {
    id: root
    color: LCPalette.TextNormal
    font.pixelSize: LCTypo.FontSizeM

    property string p_alignment: "center"  // see `LCLayout.easyAlign`
    property alias  p_bold: root.font.bold
    property alias  p_color: root.color
    property alias  p_size: root.font.pixelSize
    property alias  p_text: root.text

    Component.onCompleted: {
        LCLayout.easyAlign(root, p_alignment)
    }
}
