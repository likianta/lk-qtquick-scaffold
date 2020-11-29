import QtQuick 2.15
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

LCRectBg {
    id: root
    border.color: p_borderless ? root.color : LCPalette.BorderNormal
    border.width: 1
    color: p_color0

    property bool   p_active: false
    property bool   p_borderless: true
    property string p_color0: LCPalette.ButtonNormal
    property string p_color1: LCPalette.ButtonPressed
    // inherits:
    //      property alias p_border
    //      property alias p_radius

    states: [
        State {
            when: p_active
            PropertyChanges {
                target: root
                color: p_color1
                border.color: LCPalette.BorderSink
                border.width: 2
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
