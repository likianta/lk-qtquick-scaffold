import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

RadioButton {  // modified based on LCCheckBox
    id: root
    hoverEnabled: true
    leftPadding: LCDimension.HSpacingM
    width: LCDimension.ButtonWidthM; height: LCDimension.ButtonHeightS
    /*
        RadioButton 与 background 的 width, height 区分:
            在 RadioButton 中设置 width, height, 或者在 background 中设置
            implicitWidth, implicitHeight.
        RadioButton 与 contentItem 的 text 区分:
            在 RadioButton 中设置 text, 在 contentItem 中关联 RadioButton 的
            text.
     */

    property alias p_text: root.text
    property alias r_active: root.checked

    background: LCGhostBg {
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

        p_border.color: LCPalette.ButtonUnchecked
        p_border.width: 1
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
}