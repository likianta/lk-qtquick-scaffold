import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LKStyle/dimension.js" as LKGeometry
import "./LKStyle/motion.js" as LKMotion
import "./LKStyle/palette.js" as LKPalette
import "./LKStyle/typography.js" as LKText

TextField {
    id: _root
    horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
    leftPadding: LKGeometry.HSpacingM; rightPadding: LKGeometry.HSpacingM
    width: LKGeometry.BarWidth; height: LKGeometry.BarHeight
    
    color: LKPalette.TextNormal
    font.family: LKText.FontFamily
    font.pixelSize: LKText.FontSizeM
    placeholderTextColor: LKPalette.TextHint
    validator: RegularExpressionValidator {
        regularExpression: p_digitOnly ? /[0-9]+/ : /.*/
    }
    
    selectByMouse: true
    selectedTextColor: LKPalette.TextSelected
    selectionColor: LKPalette.TextSelection

    property bool p_digitOnly: false
    property alias p_hint: _root.placeholderText
    property alias p_text: _root.text

    property alias __active: _root.activeFocus

    background: LKRectangleBg {
        id: _bg
        // Note: If the background item has no explicit size specified, it 
        //  automatically follows the control's size. In most cases, there is no
        //  need to specify width or height for a background item.
        p_active: __active
        p_border.width: __active ? 1 : 0
        p_color0: LKPalette.EditbarNormal
        p_color1: LKPalette.EditbarFocus
    }
}
