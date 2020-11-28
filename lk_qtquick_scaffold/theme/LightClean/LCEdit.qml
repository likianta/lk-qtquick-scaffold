import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCBackground"
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo

TextField {
    id: root
    leftPadding: LCDimension.HSpacingM; rightPadding: LCDimension.HSpacingM
    width: LCDimension.BarWidth; height: LCDimension.BarHeight

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
    property alias  p_hint: root.placeholderText
    property alias  p_text: root.text

    signal clicked()

    background: LCFieldBg {
        p_active: root.activeFocus
    }

    Component.onCompleted: {
        this.pressed.connect(this.clicked)
    
        switch (p_alignment) {  // modified based on `LCText`
            case 'center':
                this.horizontalAlignment = TextInput.AlignHCenter
                this.verticalAlignment = TextInput.AlignVCenter
                break
            case 'hcenter':
                this.horizontalAlignment = TextInput.AlignHCenter
                break
            case 'htop':
                this.horizontalAlignment = TextInput.AlignHCenter
                this.verticalAlignment = TextInput.AlignTop
                break
            case 'hbottom':
                this.horizontalAlignment = TextInput.AlignHCenter
                this.verticalAlignment = TextInput.AlignBottom
                break
            case 'vcenter':
                this.verticalAlignment = TextInput.AlignVCenter
                break
            case 'vleft':
                // fall down
            case 'lcenter':
                this.horizontalAlignment = TextInput.AlignLeft
                this.verticalAlignment = TextInput.AlignVCenter
                break
            case 'vright':
                // fall down
            case 'rcenter':
                this.horizontalAlignment = TextInput.AlignRight
                this.verticalAlignment = TextInput.AlignVCenter
                break
        }
    }
}
