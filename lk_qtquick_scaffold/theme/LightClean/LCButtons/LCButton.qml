import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette
import "../LCStyle/typography.js" as LCText

Button {
    id: root
    width: LCDimension.ButtonWidthM; height: LCDimension.ButtonHeightM
    
    property bool   p_autoWidth: true
    property alias  p_borderless: _bg.p_borderless
    property string p_color: LCPalette.TextNormal
    property alias  p_text: root.text
    property alias  __active: root.pressed
    property alias  __textComp: _txt  // Access this only for special intent.
    
    background: LCButtonBg {
        id: _bg
        p_active: __active
        Component.onCompleted: {
            if (!p_borderless) {

            }
        }
    }

    contentItem: Item {
        LCText {
            id: _txt
            anchors.centerIn: parent
            p_bold: true
            p_color: root.p_color
            p_size: LCText.ButtonTextSize
            p_text: root.text
        }
    }

    Component.onCompleted: {
        if (p_autoWidth) {
            const preferredWidth = _txt.contentWidth + 40
            if (preferredWidth > root.width) {
                root.width = preferredWidth
            }
        }
    }
}
