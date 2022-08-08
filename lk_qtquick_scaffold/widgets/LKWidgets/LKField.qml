import QtQuick 2.15

Item {
    id: root
    width: pysize.field_width
    height: pysize.field_height
    clip: true

    property Component delegate: LKInput { }
    property alias     fieldItem: _loader.item
    property int       fieldWidth: 0
    property alias     text: _text.text
    property alias     textItem: _text
    property int       __spacing: pysize.spacing_l

    LKText {
        id: _text
        anchors {
            left: parent.left
            right: _loader.left
            rightMargin: root.__spacing
            verticalCenter: parent.verticalCenter
        }
        clip: true
        horizontalAlignment: Text.AlignRight
    }

    Loader {
        id: _loader
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        width: root.fieldWidth
//        height: root.height
        sourceComponent: root.delegate

        onLoaded: {
            this.item.width = Qt.binding(() => this.width)
        }

        Component.onCompleted: {
            if (this.width == 0) {
                this.width = Qt.binding(() => {
                    console.log(root.width, _text.contentWidth)
                    return root.width - _text.contentWidth - root.__spacing
                })
            }
        }
    }
}
