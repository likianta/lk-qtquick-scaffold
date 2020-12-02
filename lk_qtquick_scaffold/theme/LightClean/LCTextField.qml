import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCBackground"
import "./LCStyle/dimension.js" as LCDimension
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo
import "../../qml_helper/layout_helper.js" as LCLayout

Item {
    id: root
    implicitWidth: LCDimension.BarWidth
    implicitHeight: LCDimension.BarHeight

    property alias p_alignment: _field.p_alignment
    property alias p_hint: _field.placeholderText
    property alias p_title: _title.p_text
    property alias p_value: _field.text

    signal clicked()

    LCText {
        id: _title
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }
        width: _title.implicitWidth
    }

    TextField {
        id: _field
        anchors {
            left: _title.right
            leftMargin: LCDimension.MarginM
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
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

        background: LCFieldBg {
            p_active: _field.activeFocus
        }

        Component.onCompleted: {
            this.pressed.connect(root.clicked)
            LCLayout.easyAlign(this, p_alignment)
        }
    }
}
