import QtQuick 2.14
import "./LCStyle/geometry.js" as LCGeometry
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette

Rectangle {
    id: _root
    border.color: LCPalette.BorderNormal
    color: p_color
    radius: LCGeometry.RadiusS

    property bool p_active: false
    property alias p_border: _root.border  // Set both `p_border.width` and
    //  `p_border.color`. For LCEdit, init width = 0, color is invisible; for
    //  LCButton, init width = 1, color is visible.
    property string p_color: LCPalette.BgWhite
    property string p_pressedColor: ""
    property alias p_radius: _root.radius

    states: [
        State {
            when: p_active
            PropertyChanges {
                target: _root
                // border.width: Math.abs(_root.border.width - 1)
                color: p_pressedColor  // For LCEdit, be lighter; for LCButton,
                //  be deeper.
            }
        }
    ]
    transitions: [
        Transition {
            ColorAnimation {
                duration: LCMotion.Swift
                easing.type: Easing.OutQuart
                properties: "color"
            }
        }
    ]
}
