import QtQuick 2.14
import QtQuick.Controls 2.14
import "./Spec/geometry.js" as LCGeometry
import "./Spec/motion.js" as LCMotion
import "./Spec/palette.js" as LCPalette
import "./Spec/text.js" as LCText

Button {
    id: _root
    width: LCGeometry.ButtonWidth; height: LCGeometry.ButtonHeight

    property alias p_text: _txt.text
    property alias __pressed: _root.pressed
    property bool p_autoSize: false
    
    background: LCRectangle {
        id: _bg
        // Note: If the background item has no explicit size specified, it
        //  automatically follows the control's size. In most cases, there is no
        //  need to specify width or height for a background item.
        //anchors.centerIn: _root
        p_active: __pressed
        p_border.width: p_active ? 0 : 1
        p_color: LCPalette.ButtonNormal; p_pressedColor: LCPalette.ButtonPressed
    }

    contentItem: Item {
        LCText {
            id: _txt
            anchors.centerIn: parent
            p_bold: true
            // p_color: LCPalette.TextNormal
            p_color: __pressed ? LCPalette.TextWhite : LCPalette.TextNormal
            p_size: LCText.ButtonTextSize

            //states: [
            //    State {
            //        when: __pressed
            //        PropertyChanges {
            //            target: _txt
            //            p_color: LCPalette.TextWhite
            //        }
            //    }
            //]
            //transitions: [
            //    Transition {
            //        ColorAnimation {
            //            duration: LCMotion.Swift
            //            properties: "p_color"
            //        }
            //    }
            //]
        }
    }

    Component.onCompleted: {
        if (p_autoSize) {
            const preferredWidth = p_text.length * 10 + 20
            if (preferredWidth > _root.width) {
                _root.width = preferredWidth
            }
        }
    }
}
