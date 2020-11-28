import QtQuick 2.15
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

LCRectBg {
    id: root
    border.width: 2; border.color: root.color
    color: p_color0

    property bool   p_active: false
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
