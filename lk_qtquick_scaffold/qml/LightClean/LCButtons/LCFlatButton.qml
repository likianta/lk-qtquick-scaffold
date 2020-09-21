import QtQuick 2.14
import QtQuick.Controls 2.14
import "../LCStyle/geometry.js" as LCGeometry
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette
import "../LCStyle/text.js" as LCText

LCBaseButton {
    id: _root

    p_autoSize: true
    p_border.width: 0
    p_colorBg0: LCPalette.Transparent
    p_colorBg1: LCPalette.Transparent
    p_colorText0: LCPalette.TextNormal
    p_colorText1: LCPalette.TextHighlight

    onPressed: p_active = !p_active
}
