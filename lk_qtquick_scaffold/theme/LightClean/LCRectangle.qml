import QtQuick 2.15
import "./LCStyle/dimension.js" as LCGeometry
import "./LCStyle/palette.js" as LCPalette

Rectangle {
    id: _root
    border.width: 0; border.color: LCPalette.BorderNormal
    color: LCPalette.BgWhite
    implicitWidth: LCGeometry.BarWidth; implicitHeight: LCGeometry.BarHeight
    radius: LCGeometry.RadiusS

    property alias p_border: _root.border
    property alias p_color: _root.color
    property alias p_radius: _root.radius
}