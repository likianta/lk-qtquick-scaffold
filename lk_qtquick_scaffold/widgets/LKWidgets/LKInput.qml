import QtQuick 2.15

LKRectangle {
    id: root
    width: pysize.edit_width
    height: pysize.edit_height
    border.width: 1
    border.color: pycolor.border_normal
    color: _input.activeFocus ? pycolor.white : pycolor.transparent

    property alias activeFocus_: _input.activeFocus
    property int   cursorShape: -1
    property alias displayText: _input.displayText
    property alias focus_: _input.focus
    property alias inputMask: _input.inputMask
    property alias text: _input.text
    property alias textColor: _input.color
    property alias textHint: _placeholder.text

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

    Text {
        id: _placeholder
        anchors {
            left: parent.left
            right: parent.right
            leftMargin: 8
            rightMargin: 8
            verticalCenter: parent.verticalCenter
        }
        color: pycolor.border_normal
        visible: _placeholder.text && !_input.text
    }

    TextInput {
        id: _input
        anchors.fill: _placeholder
        clip: true
        selectByMouse: true
        onTextEdited: {
//            console.log(this.text, this.displayText)
            root.textEdited(this.text)
        }
    }
}
