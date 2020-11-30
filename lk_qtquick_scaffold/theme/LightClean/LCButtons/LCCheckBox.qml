import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette

CheckBox {
    id: root
    implicitWidth: LCDimension.ButtonWidthM
    implicitHeight: LCDimension.ButtonHeightS
    // implicitWidth: root.contentWidth
    // implicitHeight: root.contentHeight
    hoverEnabled: true
    leftPadding: LCDimension.HSpacingM

    property alias p_text: root.text
    property alias r_active: root.checked

    background: LCGhostBg {
        // implicitWidth: LCDimension.ButtonWidthM
        // implicitHeight: LCDimension.ButtonHeightS
        p_active: r_active
        p_hovered: root.hovered
    }

    contentItem: LCText {
        id: _txt
        anchors.left: _indicator.right
        anchors.leftMargin: LCDimension.HSpacingS
        p_alignment: "vcenter"
        p_text: root.text
    }

    indicator: LCRectangle {
        id: _indicator
        anchors.left: parent.left
        anchors.leftMargin: LCDimension.HSpacingS
        anchors.verticalCenter: parent.verticalCenter
        implicitWidth: LCDimension.IndicatorCheckWidth
        implicitHeight: LCDimension.IndicatorCheckHeight
        clip: true

        p_border.width: 1
        p_border.color: LCPalette.ButtonUnchecked
        p_color: LCPalette.Transparent
        p_radius: LCDimension.IndicatorCheckRadius

        Image {
            anchors.fill: parent
            anchors.margins: LCDimension.SpacingS
            source: '../rss/check-white.svg'
            visible: r_active
        }

        states: [
            State {
                when: r_active
                PropertyChanges {
                    target: _indicator
                    p_border.color: LCPalette.ButtonChecked
                    p_color: LCPalette.ButtonChecked
                }
            }
        ]
    }
}