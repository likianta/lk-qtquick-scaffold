import QtQuick 2.14
import QtQuick.Controls 2.14
import "./LCStyle/geometry.js" as LCGeometry
import "./LCStyle/palette.js" as LCPalette

CheckBox {
    id: _root
    // height: LCGeometry.BarHeightS

    property alias p_text: _txt.p_text
    property alias __active: _root.checked

    // onCheckedChanged: {
    //     console.log("LCCheckBox", "check changed", __active)
    // }

    contentItem: LCText {
        id: _txt
        anchors.fill: parent
        anchors.leftMargin: _indicator.width + LCGeometry.HSpacingS
        p_alignment: "vcenter"
        p_bold: __active
    }

    indicator: LCRectangle {
        id: _indicator
        anchors.verticalCenter: parent.verticalCenter
        width: LCGeometry.IndicatorCheckWidth; height: LCGeometry.IndicatorCheckHeight

        p_border.width: 1
        p_radius: LCGeometry.IndicatorCheckRadius

        LCRectangleBg {
            id: _indicator_filler
            anchors.fill: parent
            // anchors.margins: 1

            p_active: __active
            p_border.width: 0
            p_color: "transparent"; p_pressedColor: LCPalette.ButtonChecked
            p_radius: parent.radius
        }
    }
}