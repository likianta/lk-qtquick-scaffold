import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette

RadioButton {  // modified based on LCCheckBox
    id: root
    // implicitWidth: see `Component.onCompleted`
    implicitHeight: LCDimension.ButtonHeightS
    hoverEnabled: true
    leftPadding: LCDimension.HSpacingM
    rightPadding: LCDimension.HSpacingS

    property alias p_text: root.text
    property alias r_active: root.checked

    background: LCGhostBg {
        id: _bg
        p_active: r_active
        p_hovered: root.hovered
    }

    contentItem: LCText {
        id: _txt
        anchors.left: _outer.right
        anchors.leftMargin: LCDimension.HSpacingS
        p_alignment: "vcenter"
        p_text: root.text
    }

    indicator: LCOval {
        id: _outer
        anchors.left: parent.left
        anchors.leftMargin: LCDimension.HSpacingS
        anchors.verticalCenter: parent.verticalCenter
        clip: true

        p_border.width: 1
        p_border.color: LCPalette.ButtonUnchecked
        p_color: LCPalette.Transparent
        p_radius: LCDimension.IndicatorRadioRadius

        LCOval {
            id: _inner
            anchors.centerIn: parent
            visible: r_active
            p_radius: parent.p_radius - LCDimension.SpacingS
        }

        states: [
            State {
                when: r_active
                PropertyChanges {
                    target: _inner
                    p_border.color: LCPalette.ButtonChecked
                    p_color: LCPalette.ButtonChecked
                }
                PropertyChanges {
                    target: _outer
                    p_border.color: LCPalette.BorderSink
                    p_border.width: 2
                }
            }
        ]
    }

    Component.onCompleted: {
        root.implicitWidth = root.leftPadding + root.rightPadding +
            (_txt.x + _txt.implicitWidth - _outer.x)
    }
}