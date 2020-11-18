import QtQuick 2.15
import QtQuick.Window 2.15
import "./LKStyle/dimension.js" as LKDimension
import "./LKStyle/palette.js" as LKPalette

Window {
    id: _root
    color: LKPalette.BgWhite
    visible: true
    width: LKDimension.WinWidth; height: LKDimension.WinHeight

    property alias p_color: _root.color

    Component.onCompleted: {
        // TODO: iterate children recursively, set child items which has
        PyHooks.scanning_qml_tree(_root)
        // TODO: enumerate methods related to PyHandler.
    }
}
