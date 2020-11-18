import QtQuick 2.15
import "./LKStyle/dimension.js" as LKGeometry
import "./LKStyle/palette.js" as LKPalette

Rectangle {
    id: _root
    border.width: 0; border.color: LKPalette.BorderNormal
    color: LKPalette.BgWhite
    implicitWidth: LKGeometry.BarWidth; implicitHeight: LKGeometry.BarHeight
    radius: LKGeometry.RadiusS

    property alias p_border: _root.border
    property alias p_color: _root.color
    property alias p_radius: _root.radius
}
