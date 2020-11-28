import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

CheckBox {
    id: root
    hoverEnabled: true
    leftPadding: LCDimension.HSpacingM
    width: LCDimension.ButtonWidthM; height: LCDimension.ButtonHeightS

    property alias p_text: _txt.p_text
    property alias __active: root.checked

    background: LCRectangle {
        id: _bg
        p_border.width: 0
        p_color: LCPalette.Transparent

        states: [
            State {
                when: !__active && root.hovered
                PropertyChanges {
                    target: _bg
                    p_border.width: 1
                    p_color: LCPalette.TranslucentLH
                }
            },
            State {
                when: root.hovered
                PropertyChanges {
                    target: _bg
                    p_border.width: 1
                }
            }
        ]
    }

    contentItem: LCText {
        id: _txt
        anchors.left: _indicator.right
        anchors.leftMargin: LCDimension.HSpacingS
        p_alignment: "vcenter"
    }

    indicator: LCRectangle {
        id: _indicator
        anchors.left: parent.left
        anchors.leftMargin: LCDimension.HSpacingS
        anchors.verticalCenter: parent.verticalCenter
        clip: true
        width: LCDimension.IndicatorCheckWidth; height: LCDimension.IndicatorCheckHeight

        p_border.color: LCPalette.ButtonUnchecked
        p_border.width: 1
        p_color: LCPalette.Transparent
        p_radius: LCDimension.IndicatorCheckRadius

        states: [
            State {
                when: __active
                PropertyChanges {
                    target: _indicator
                    p_border.color: LCPalette.ButtonChecked
                    p_color: LCPalette.ButtonChecked
                }
            }
        ]
    }
}