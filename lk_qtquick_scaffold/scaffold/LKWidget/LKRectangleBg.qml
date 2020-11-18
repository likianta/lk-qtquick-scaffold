import QtQuick 2.15
import "./LKStyle/dimension.js" as LKGeometry
import "./LKStyle/motion.js" as LKMotion
import "./LKStyle/palette.js" as LKPalette

Rectangle {
    id: _root
    border.color: LKPalette.BorderNormal
    color: p_color0
    radius: LKGeometry.RadiusS

    property bool p_active: false
    property alias p_border: _root.border  // Set both `p_border.width` and
    //  `p_border.color`. For LKEdit, init width = 0, color is invisible; for
    //  LKButton, init width = 1, color is visible.
    property string p_color0: LKPalette.BgWhite
    property string p_color1: LKPalette.BgWhite
    property alias p_radius: _root.radius

    states: [
        State {
            when: p_active
            PropertyChanges {
                target: _root
                // border.width: Math.abs(_root.border.width - 1)
                color: p_color1  // For LKEdit, be lighter; for LKButton, be
                //      deeper.
            }
        }
    ]
    transitions: [
        Transition {
            ColorAnimation {
                duration: LKMotion.Swift
                easing.type: Easing.OutQuart
                properties: "color"
            }
        }
    ]
}
