import QtQuick 2.15
import QtQuick.Window 2.15
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/palette.js" as LCPalette

Window {
    id: root
    color: LCPalette.BgWhite
    visible: true
    width: LCDimension.WinWidth; height: LCDimension.WinHeight

    property alias p_color: root.color

    // Component.onCompleted: {
    //     // TODO: iterate children recursively, set child items which has
    //     PyHooks.scanning_qml_tree(_root)
    //     // TODO: enumerate methods related to PyHandler.
    // }
}
