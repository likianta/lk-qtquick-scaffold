import QtQuick 2.14
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/text.js" as LCText

Text {
    id: _root
    color: LCPalette.TextNormal
    font.family: LCText.FontFamily
    font.pixelSize: LCText.FontSizeM
    horizontalAlignment: Text.AlighHCenter; verticalAlignment: Text.AlignVCenter

    property alias p_bold: _root.font.bold
    property alias p_color: _root.color
    property alias p_size: _root.font.pixelSize
    property alias p_text: _root.text
}
