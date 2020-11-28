import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCBackground"
import "./LCStyle/dimension.js" as LCGeometry
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo

TextField {
    id: _root
    leftPadding: LCGeometry.HSpacingM; rightPadding: LCGeometry.HSpacingM
    width: LCGeometry.BarWidth; height: LCGeometry.BarHeight

    font.pixelSize: LCTypo.FontSizeM
    placeholderTextColor: LCPalette.TextHint
    validator: RegularExpressionValidator {
        regularExpression: p_digitOnly ? /[0-9]+/ : /.*/
    }
    
    selectByMouse: true
    selectedTextColor: LCPalette.TextSelected
    selectionColor: LCPalette.TextSelection

    property string p_alignment: 'center'
    property bool   p_digitOnly: false
    property alias  p_hint: _root.placeholderText
    property alias  p_text: _root.text
    property alias  __active: _root.activeFocus

    signal clicked()

    background: LCFieldBg {
        p_active: __active
    }

    Component.onCompleted: {
        this.pressed.connect(this.clicked)
    
        if (p_alignment == 'center') {
            _root.horizontalAlignment = Text.AlignHCenter
            _root.verticalAlignment = Text.AlignVCenter
        } else if (p_alignment == 'hcenter') {
            _root.horizontalAlignment = Text.AlignHCenter
        } else if (p_alignment == 'htop') {
            _root.horizontalAlignment = Text.AlignHCenter
            _root.verticalAlignment = Text.AlignTop
        } else if (p_alignment == 'hbottom') {
            _root.horizontalAlignment = Text.AlignHCenter
            _root.verticalAlignment = Text.AlignBottom
        } else if (p_alignment == 'vcenter') {
            _root.verticalAlignment = Text.AlignVCenter
        } else if (p_alignment == 'vleft') {
            _root.horizontalAlignment = Text.AlignLeft
            _root.verticalAlignment = Text.AlignVCenter
        } else if (p_alignment == 'vright') {
            _root.horizontalAlignment = Text.AlignRight
            _root.verticalAlignment = Text.AlignVCenter
        }
    }
}
