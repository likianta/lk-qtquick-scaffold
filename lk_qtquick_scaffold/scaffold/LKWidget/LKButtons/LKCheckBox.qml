import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LKStyle/dimension.js" as LKDimension
import "../LKStyle/palette.js" as LKPalette

CheckBox {
    id: _root
    // height: LKDimension.BarHeightS

    property alias p_text: _txt.p_text
    property alias __active: _root.checked
    
    // onCheckedChanged: {
    //     console.log("LKCheckBox", "check changed", __active)
    // }
    
    background: LKRectangle {
        id: _bg
        implicitWidth: LKDimension.ButtonWidthM; implicitHeight: LKDimension.ButtonHeightM
        p_border.width: 0
        p_color: "transparent"
    }

    contentItem: LKText {
        id: _txt
        anchors.fill: parent
        anchors.leftMargin: _indicator.width + LKDimension.HSpacingS
        p_alignment: "vcenter"
        p_bold: __active
    }

    indicator: LKRectangle {
        id: _indicator
        anchors.verticalCenter: parent.verticalCenter
        clip: true
        width: LKDimension.IndicatorCheckWidth; height: LKDimension.IndicatorCheckHeight

        p_border.width: 1; p_border.color: __active ? LKPalette.ButtonChecked : LKPalette.ButtonUnchecked
        p_radius: LKDimension.IndicatorCheckRadius

        LKRectangleBg {
            id: _indicator_filler
            anchors.fill: parent
            // anchors.margins: 1

            p_active: __active
            p_border.width: 0
            p_color0: LKPalette.Transparent; p_color1: LKPalette.ButtonChecked
            p_radius: parent.radius
        }
    }
}