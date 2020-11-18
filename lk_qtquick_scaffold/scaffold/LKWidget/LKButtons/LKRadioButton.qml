import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LKStyle/dimension.js" as LKGeometry
import "../LKStyle/palette.js" as LKPalette

RadioButton {
    id: _root
    height: LKGeometry.BarHeightS

    property alias p_text: _txt.p_text
    property alias __active: _root.checked

    contentItem: LKText {
        id: _txt
        anchors.fill: parent
        anchors.leftMargin: _indicator.width + LKGeometry.HSpacingS
        p_alignment: "vcenter"
        p_bold: __active
    }
    indicator: Rectangle {
        id: _indicator
        anchors.verticalCenter: parent.verticalCenter
        border.width: 1; border.color: LKPalette.BorderNormal
        radius: LKGeometry.IndicatorRadioRadius
        width: LKGeometry.IndicatorRadioWidth; height: LKGeometry.IndicatorRadioHeight

        Rectangle {
            anchors.fill: parent
            anchors.margins: 1
            color: __active ? LKPalette.ButtonPressed : "transparent"
            radius: parent.radius
        }
    }
}