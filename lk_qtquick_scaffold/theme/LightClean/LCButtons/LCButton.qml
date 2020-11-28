import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCGeometry
import "../LCStyle/motion.js" as LCMotion
import "../LCStyle/palette.js" as LCPalette
import "../LCStyle/typography.js" as LCText

Button {
    id: root
    width: LCGeometry.ButtonWidthM; height: LCGeometry.ButtonHeightM
    
    property bool  p_autoWidth: true
    property alias p_text: root.text
    property alias __active: root.pressed
    
    background: LCButtonBg {
        p_active: __active
    }

    contentItem: Item {
        LCText {
            id: _txt
            anchors.centerIn: parent
            p_bold: true
            p_color: LCPalette.TextNormal
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
