import QtQuick 2.15
import QtQuick.Controls 2.15
import "../LKStyle/palette.js" as LKPalette

LKBaseButton {
    id: _root
    flat: true
    hoverEnabled: true

    p_autoSize: true
    p_border.width: 0
    p_colorBg0: LKPalette.Transparent
    p_colorBg1: LKPalette.Transparent
    p_colorText0: LKPalette.TextNormal
    p_colorText1: LKPalette.TextHighlight
    // more:
    //      p_active
    //      p_height
    //      p_text
    //      p_width

    __bg.color: {
        if (_root.hovered) {
            return LKPalette.ButtonHovered
        } else if (_root.pressed) {
            return LKPalette.ButtonPressed
        } else if (p_active) {
            return p_colorBg0
        } else {
            return p_colorBg1
        }
    }

    onPressed: p_active = !p_active
}
