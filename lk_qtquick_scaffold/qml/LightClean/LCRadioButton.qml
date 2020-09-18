import QtQuick 2.14
import QtQuick.Controls 2.14
import "./LCStyle/geometry.js" as LCGeometry
import "./LCStyle/palette.js" as LCPalette

RadioButton {
    id: _root
    height: LCGeometry.BarHeightS

    property alias p_text: _txt.p_text
    property alias __active: _root.checked
    property alias __indicatorSize: _txt.height

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
        width: LCGeometry.ButtonRadioWidth; height: LCGeometry.ButtonRadioHeight
        radius: width / 2

        Rectangle {
            anchors.fill: parent
            anchors.margins: 1
            color: __active ? LCPalette.ButtonPressed : "transparent"
            radius: parent.radius
        }
    }

    Component.onCompleted: {
        console.log(
            "LCRadioButton",
            _root.width, _root.height,
            _txt.width, _txt.height,
            _indicator.width, _indicator.height,
        )
    }
}