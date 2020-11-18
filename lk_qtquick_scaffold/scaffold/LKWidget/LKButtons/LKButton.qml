import QtQuick 2.15
import QtQuick.Controls 2.15
import "../"
import "../LKStyle/dimension.js" as LKGeometry
import "../LKStyle/motion.js" as LKMotion
import "../LKStyle/palette.js" as LKPalette
import "../LKStyle/typography.js" as LKText

Button {
    id: _root
    // height: LKGeometry.ButtonHeightM

    property bool p_autoSize: true
    property alias p_border: _bg.p_border  // you can set `p_border.width: 0` to
    //      make button frameless.
    property alias p_text: _txt.text
    property alias p_width: _bg.implicitWidth; property alias p_height: _bg.implicitHeight
    property alias __active: _root.pressed

    background: LKRectangleBg {
        id: _bg
        // Note: If the background item has no explicit size specified, it
        //      automatically follows the control's size. In most cases, there
        //      is no need to specify width or height for a background item.
        implicitWidth: LKGeometry.ButtonWidthM; implicitHeight: LKGeometry.ButtonHeightM
        p_active: __active
        p_border.width: __active ? 0 : 1
        p_color0: LKPalette.ButtonNormal; p_color1: LKPalette.ButtonPressed
    }

    contentItem: Item {
        LKText {
            id: _txt
            anchors.centerIn: parent
            p_bold: true
            // p_color: LKPalette.TextNormal
            p_color: __active ? LKPalette.TextWhite : LKPalette.TextNormal
            p_size: LKText.ButtonTextSize

            // states: [
            //     State {
            //         when: __active
            //         PropertyChanges {
            //             target: _txt
            //             p_color: LKPalette.TextWhite
            //         }
            //     }
            // ]
            // transitions: [
            //     Transition {
            //         ColorAnimation {
            //             duration: LKMotion.Swift
            //             properties: "p_color"
            //         }
            //     }
            // ]
        }
    }

    Component.onCompleted: {
        if (p_autoSize) {
            const preferredWidth = _txt.contentWidth + 20
            if (preferredWidth > _root.width) {
                p_width = preferredWidth
            }
        }
    }
}
