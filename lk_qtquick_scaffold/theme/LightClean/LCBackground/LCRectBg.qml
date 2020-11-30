import QtQuick 2.15
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette

Rectangle {
    id: root
    implicitWidth: LCDimension.BarWidth
    implicitHeight: LCDimension.BarHeight

    border.width: 0
    border.color: LCPalette.BorderNormal
    color: LCPalette.BgWhite
    radius: LCDimension.RadiusM

    property alias p_border: root.border
    property alias p_color: root.color
    property alias p_radius: root.radius
}
