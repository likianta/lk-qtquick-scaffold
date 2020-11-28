import QtQuick 2.15
import QtQuick.Controls 2.15

import "../"
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
    
    background: LCRectangleBg {
        id: _bg
        p_active: __active
        p_border.color: __active ? LCPalette.BorderSink : p_color0
        p_border.width: 2
        p_color0: LCPalette.ButtonNormal
        p_color1: LCPalette.ButtonPressed
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
