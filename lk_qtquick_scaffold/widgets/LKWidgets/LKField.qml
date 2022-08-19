import QtQuick 2.15

Item {
    id: root
    width: widthA + widthB + __spacing
    height: pysize.field_height
    clip: true

    property Component delegate: LKInput { }
    property alias     fieldItem: _loader.item
    property int       fieldWidth: 0
    property alias     text: _text.text
    property alias     textItem: _text
    property int       widthA: 0
    property int       widthB: 0
    property int       __spacing: pysize.spacing_l

    LKText {
        id: _text
        anchors {
            right: _loader.left
            rightMargin: root.__spacing
            verticalCenter: parent.verticalCenter
        }
        width: root.widthA
        clip: true
        horizontalAlignment: Text.AlignRight
    }

    Loader {
        id: _loader
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        width: root.widthB
//        height: root.height
        sourceComponent: root.delegate

        onLoaded: {
            this.item.width = Qt.binding(() => this.width)
        }
    }

    Component.onCompleted: {
        if (widthA == 0) {
            widthA = pylayout.calc_content_width(_text.text)
        }
        if (widthB == 0) {
            widthB = pysize.field_width
        }
    }
}
