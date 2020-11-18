import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LKStyle/dimension.js" as LKDimension
import "../LKStyle/palette.js" as LKPalette

RadioButton {
    id: _root
    height: LKDimension.BarHeightS

    property bool  p_showIndicator: true
    property alias p_text: _txt.p_text
    property alias r_active: _root.checked

    contentItem: LKRectangle {
        id: _bgrect
        anchors.fill: parent
        color: "transparent"
        radius: parent.radius

        LKText {
            anchors {
                left: parent.left
                leftMargin: LKDimension.HSpacingS
                verticalCenter: parent.verticalCenter
            }
            p_bold: r_active
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                _bgrect.color = r_active ? LKPalette.ButtonPressed : LKPalette.ButtonHovered
            }
            onExited: {
                _bgrect.color = r_active ? LKPalette.ButtonPressed : "transparent"
            }
            onClicked: {
                _root.clicked()
                _bgrect.color = r_active ? LKPalette.ButtonPressed : "transparent"
            }
        }
    }
    indicator: Item {}

    /*
        contentItem: LKText {
            id: _txt
            anchors.fill: parent
            anchors.leftMargin: _indicator.width + LKDimension.HSpacingS
            p_alignment: "vcenter"
            p_bold: r_active
        }
        indicator: Rectangle {
            id: _indicator
            anchors.verticalCenter: parent.verticalCenter
            border.width: 1; border.color: LKPalette.BorderNormal
            radius: LKDimension.IndicatorRadioRadius
            width: LKDimension.IndicatorRadioWidth; height: LKDimension.IndicatorRadioHeight

            Rectangle {
                anchors.fill: parent
                anchors.margins: 1
                color: r_active ? LKPalette.ButtonPressed : "transparent"
                radius: parent.radius
            }
        }
    */
}