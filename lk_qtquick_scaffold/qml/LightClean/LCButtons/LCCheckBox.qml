import QtQuick 2.14
import QtQuick.Controls 2.14
import "../"
import "../LCStyle/geometry.js" as LCGeometry
import "../LCStyle/palette.js" as LCPalette

CheckBox {
    id: _root
    // height: LCGeometry.BarHeightS

    property alias p_text: _txt.p_text
    property alias __active: _root.checked

    // onCheckedChanged: {
    //     console.log("LCCheckBox", "check changed", __active)
    // }

    background: LCRectangle {
        id: _bg
        implicitWidth: LCGeometry.ButtonWidthM; implicitHeight: LCGeometry.ButtonHeightM
        p_border.width: 0
        p_color: "transparent"
    }

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

        p_border.width: 1; p_border.color: __active ? LCPalette.ButtonChecked : LCPalette.ButtonUnchecked
        p_radius: LCGeometry.IndicatorCheckRadius

        LCRectangleBg {
            id: _indicator_filler
            anchors.fill: parent
            // anchors.margins: 1

            p_active: __active
            p_border.width: 0
            p_color0: LCPalette.Transparent; p_color1: LCPalette.ButtonChecked
            p_radius: parent.radius
        }
    }
}