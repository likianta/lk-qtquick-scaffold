import QtQuick 2.15
import "./LCStyle/dimension.js" as LCGeometry
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette

Rectangle {
    id: root
    border.color: LCPalette.BorderNormal
    color: p_color0
    radius: LCGeometry.RadiusM

    property bool   p_active: false
    property alias  p_border: root.border  // Set both `p_border.width` and
    //  `p_border.color`. For LCEdit, init width = 0, color is invisible; for
    //  LCButton, init width = 1, color is visible.
    property string p_color0: LCPalette.BgWhite
    property string p_color1: LCPalette.BgWhite
    property alias  p_radius: root.radius

    states: [
        State {
            when: p_active
            PropertyChanges {
                target: root
                color: p_color1
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
