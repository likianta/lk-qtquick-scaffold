import QtQuick 2.14
import QtQuick.Controls 2.14
import "../"
import "../LCStyle/geometry.js" as LCGeometry
import "../LCStyle/palette.js" as LCPalette

RadioButton {
    id: _root
    height: LCGeometry.BarHeightS

    property alias p_text: _txt.p_text
    property alias __active: _root.checked

    contentItem: LCText {
        id: _txt
        anchors.fill: parent
        anchors.leftMargin: _indicator.width + LCGeometry.HSpacingS
        p_alignment: "vcenter"
        p_bold: __active
    }
    indicator: Rectangle {
        id: _indicator
        anchors.verticalCenter: parent.verticalCenter
        border.width: 1; border.color: LCPalette.BorderNormal
        radius: LCGeometry.IndicatorRadioRadius
        width: LCGeometry.IndicatorRadioWidth; height: LCGeometry.IndicatorRadioHeight

        Rectangle {
            anchors.fill: parent
            anchors.margins: 1
            color: __active ? LCPalette.ButtonPressed : "transparent"
            radius: parent.radius
        }
    }
}