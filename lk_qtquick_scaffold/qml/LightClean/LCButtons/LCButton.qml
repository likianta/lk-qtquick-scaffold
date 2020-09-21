import QtQuick 2.14
import QtQuick.Controls 2.14
import "../"
import "../LCStyle/geometry.js" as LCGeometry
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette
import "../LCStyle/text.js" as LCText

Button {
    id: _root
    // height: LCGeometry.ButtonHeightM

    property bool p_autoSize: true
    property alias p_border: _bg.p_border  // you can set `p_border.width: 0` to
    //      make button frameless.
    property alias p_text: _txt.text
    property alias p_width: _bg.implicitWidth; property alias p_height: _bg.implicitHeight
    property alias __active: _root.pressed

    background: LCRectangleBg {
        id: _bg
        // Note: If the background item has no explicit size specified, it
        //      automatically follows the control's size. In most cases, there
        //      is no need to specify width or height for a background item.
        implicitWidth: LCGeometry.ButtonWidthM; implicitHeight: LCGeometry.ButtonHeightM
        p_active: __active
        p_border.width: __active ? 0 : 1
        p_color0: LCPalette.ButtonNormal; p_color1: LCPalette.ButtonPressed
    }

    contentItem: Item {
        LCText {
            id: _txt
            anchors.centerIn: parent
            p_bold: true
            // p_color: LCPalette.TextNormal
            p_color: __active ? LCPalette.TextWhite : LCPalette.TextNormal
            p_size: LCText.ButtonTextSize

            // states: [
            //     State {
            //         when: __active
            //         PropertyChanges {
            //             target: _txt
            //             p_color: LCPalette.TextWhite
            //         }
            //     }
            // ]
            // transitions: [
            //     Transition {
            //         ColorAnimation {
            //             duration: LCMotion.Swift
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
