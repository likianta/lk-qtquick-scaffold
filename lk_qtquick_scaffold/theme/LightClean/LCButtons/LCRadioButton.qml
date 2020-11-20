import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/palette.js" as LCPalette

RadioButton {
    id: _root
    height: LCDimension.BarHeightS

    property bool  p_showIndicator: true
    property alias p_text: _txt.p_text
    property alias r_active: _root.checked

    contentItem: LCRectangle {
        id: _bgrect
        anchors.fill: parent
        color: "transparent"
        radius: parent.radius

        LCText {
            anchors {
                left: parent.left
                leftMargin: LCDimension.HSpacingS
                verticalCenter: parent.verticalCenter
            }
            p_bold: r_active
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                _bgrect.color = r_active ? LCPalette.ButtonPressed : LCPalette.ButtonHovered
            }
            onExited: {
                _bgrect.color = r_active ? LCPalette.ButtonPressed : "transparent"
            }
            onClicked: {
                _root.clicked()
                _bgrect.color = r_active ? LCPalette.ButtonPressed : "transparent"
            }
        }
    }
    indicator: Item {}

    /*
        contentItem: LCText {
            id: _txt
            anchors.fill: parent
            anchors.leftMargin: _indicator.width + LCDimension.HSpacingS
            p_alignment: "vcenter"
            p_bold: r_active
        }
        indicator: Rectangle {
            id: _indicator
            anchors.verticalCenter: parent.verticalCenter
            border.width: 1; border.color: LCPalette.BorderNormal
            radius: LCDimension.IndicatorRadioRadius
            width: LCDimension.IndicatorRadioWidth; height: LCDimension.IndicatorRadioHeight

            Rectangle {
                anchors.fill: parent
                anchors.margins: 1
                color: r_active ? LCPalette.ButtonPressed : "transparent"
                radius: parent.radius
            }
        }
    */
}