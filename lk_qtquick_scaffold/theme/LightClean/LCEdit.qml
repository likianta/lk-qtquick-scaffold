import QtQuick 2.15
import QtQuick.Controls 2.15

import "./LCBackground"
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo

import "../../qml_helper/layout_helper.js" as LCLayout

TextField {
    id: root
    implicitWidth: LCDimension.BarWidth
    implicitHeight: LCDimension.BarHeight

    leftPadding: LCDimension.HSpacingM
    rightPadding: LCDimension.HSpacingM
    font.pixelSize: LCTypo.FontSizeM
    placeholderTextColor: LCPalette.TextHint
    selectByMouse: true
    selectedTextColor: LCPalette.TextSelected
    selectionColor: LCPalette.TextSelection

    /*  Tip: How to use `validator` property?
            TextField {
                validator: RegularExpressionValidator {
                    regularExpression: p_digitOnly ? /[0-9]+/ : /.* /
                }
            }
        Note: This  wont be introduced into LCEdit, but you can do it
        yourself by following the tips above.
     */

    property string p_alignment: 'center'  // see `LCLayout.easyAlign`
    property alias  p_hint: root.placeholderText
    property alias  p_text: root.text

    signal clicked()

    background: LCFieldBg {
        p_active: root.activeFocus
    }

    Component.onCompleted: {
        this.pressed.connect(this.clicked)
        LCLayout.easyAlign(root, p_alignment)
    }
}
