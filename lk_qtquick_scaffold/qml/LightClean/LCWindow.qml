import QtQuick 2.14
import QtQuick.Window 2.14
import "./LCStyle/geometry.js" as LCGeometry
import "./LCStyle/palette.js" as LCPalette

Window {
    id: _root
    color: LCPalette.BgWhite
    visible: true
    width: LCGeometry.WinWidth; height: LCGeometry.WinHeight

    property alias p_color: _root.color
}
