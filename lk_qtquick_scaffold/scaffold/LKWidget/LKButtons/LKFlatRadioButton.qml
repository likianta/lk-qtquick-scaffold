import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LKStyle/dimension.js" as LKGeometry
import "../LKStyle/palette.js" as LKPalette

RadioButton {
    id: _root
    hoverEnabled: true

    // p_colorBg0: LKPalette.Transparent
    // p_colorBg1: LKPalette.Transparent
    property alias p_text: _txt.p_text
    property alias __active: _root.checked

    background: LKRectangleBg {
        id: _bg
        color: {
            if (_root.hovered) {
                return LKPalette.ButtonHovered
            } else if (_root.pressed) {
                return LKPalette.ButtonPressed
            } else {
                return LKPalette.Transparent
            }
        }
        implicitWidth: LKGeometry.ButtonWidthM; implicitHeight: LKGeometry.ButtonHeightM

        // p_active: __active
        p_border.width: 0
        // p_color0: _root.p_colorBg0
        // p_color1: _root.p_colorBg1
    }
    contentItem: LKText {
        id: _txt
        anchors.fill: parent
        anchors.leftMargin: LKGeometry.HSpacingS
        p_alignment: "vcenter"
        p_bold: false
        p_color: __active ? LKPalette.TextHighlight : LKPalette.TextNormal
    }
    indicator: Item {}
}