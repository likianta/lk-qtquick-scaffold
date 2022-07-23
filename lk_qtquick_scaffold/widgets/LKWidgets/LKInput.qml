import QtQuick 2.15

LKRectangle {
    id: root
    width: pysize.edit_width
    height: pysize.edit_height
    border.width: 1
    border.color: _input.activeFocus ? colorBorderActive : colorBorderDefault
    color: _input.activeFocus ? colorBgActive : colorBgDefault

    property alias  activeFocus_: _input.activeFocus
    property string colorBgDefault: pycolor.input_bg_default
    property string colorBgActive: pycolor.input_bg_active
    property string colorBorderDefault: pycolor.input_border_default
    property string colorBorderActive: pycolor.input_border_active
    property string colorBottomHighlight: pycolor.input_indicator_active
    property int    cursorShape: -1
    property alias  displayText: _input.displayText
    property alias  focus_: _input.focus
    property alias  inputMask: _input.inputMask
    property bool   showIndicator: false
//    property bool   showIndicator: Boolean(colorBottomHighlight)
    property alias  text: _input.text
    property alias  textColor: _input.color
    property alias  textHint: _placeholder.text

    signal textEdited(string text)

    Loader {
        // a workaround for adjusting cursor shape
        id: _loader
        anchors.fill: parent

        Component {
            id: _cursor_shape_patch
            MouseArea {
                anchors.fill: parent
                cursorShape: root.cursorShape
            }
        }

        Component.onCompleted: {
            if (root.cursorShape != -1) {
                _loader.sourceComponent = _cursor_shape_patch
            }
        }
    }

    LKText {
        id: _placeholder
        visible: _placeholder.text && !_input.text
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: 8
            rightMargin: 8
            verticalCenter: parent.verticalCenter
        }
        color: pycolor.text_hint
    }

    TextInput {
        id: _input
        anchors.fill: _placeholder
        clip: true
        color: pycolor.text_default
        font.family: pyfont.font_default
        font.pixelSize: pyfont.size_m
        selectByMouse: true
        onTextEdited: {
//            console.log(this.text, this.displayText)
            root.textEdited(this.text)
        }
    }

    Rectangle {
        id: _bottom_highlight
        visible: root.showIndicator
        anchors.bottom: parent.bottom
//        anchors.bottomMargin: 1
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width - 2
        height: _input.activeFocus ? 2 : 0
        radius: parent.radius
        color: root.colorBottomHighlight
    }
}
