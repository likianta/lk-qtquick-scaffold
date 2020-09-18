import QtQuick 2.14
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/text.js" as LCText

Text {
    id: _root
    color: LCPalette.TextNormal
    font.family: LCText.FontFamily
    font.pixelSize: LCText.FontSizeM

    property string p_alignment: "center"  // [center|hcenter|vcenter]
    property alias p_bold: _root.font.bold
    property alias p_color: _root.color
    property alias p_size: _root.font.pixelSize
    property alias p_text: _root.text

    Component.onCompleted: {
        if (p_alignment == 'center') {
            _root.horizontalAlignment = Text.AlignHCenter
            _root.verticalAlignment = Text.AlignVCenter
        } else if (p_alignment == 'hcenter') {  // not often used
            _root.horizontalAlignment = Text.AlignHCenter
        } else if (p_alignment == 'vcenter') {
            _root.verticalAlignment = Text.AlignVCenter
        }
    }
}
