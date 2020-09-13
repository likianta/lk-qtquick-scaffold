import QtQuick 2.14
import QtQuick.Controls 2.14
import "./Spec/geometry.js" as LCGeometry
import "./Spec/motion.js" as LCMotion
import "./Spec/palette.js" as LCPalette
import "./Spec/text.js" as LCText

TextField {
    id: _root
    horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
    leftPadding: LCGeometry.HSpacingM; rightPadding: LCGeometry.HSpacingM
    width: LCGeometry.BarWidth; height: LCGeometry.BarHeight
    
    color: LCPalette.TextNormal
    font.family: LCText.FontFamily
    font.pixelSize: LCText.FontSizeM
    placeholderTextColor: LCPalette.TextHint
    validator: RegularExpressionValidator {
        regularExpression: p_digitOnly ? /[0-9]+/ : /.*/
    }
    
    selectByMouse: true
    selectedTextColor: LCPalette.TextSelected
    selectionColor: LCPalette.TextSelection

    property alias p_hint: _root.placeholderText
    property alias p_text: _root.text
    property bool p_digitOnly: false

    property alias __active: _root.activeFocus

    background: LCRectangle {
        id: _bg
        // Note: If the background item has no explicit size specified, it 
        //  automatically follows the control's size. In most cases, there is no
        //  need to specify width or height for a background item.
        p_active: __active
        p_border.width: __active ? 1 : 0
        p_color: LCPalette.EditbarNormal
        p_pressedColor: LCPalette.EditbarFocus
    }
}
