import QtQuick 2.15
import "./LKStyle/palette.js" as LKPalette

Rectangle {
    id: _root
    // border.width: 1; border.color: LKPalette.BorderNormal
    color: LKPalette.BorderNormal
    width: 1; height: 1

    property alias p_color: _root.color
    property string p_orientation: 'horizontal'

    Component.onCompleted: {
        switch (p_orientation) {
            case "h":
                // downside
            case "horizontal":
                _root.width = parent.width
                break
            case "v":
                // downside
            case "vertical":
                _root.height = parent.height
                break
        }
    }
}
