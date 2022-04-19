import QtQuick

Rectangle {
    width: 0
    height: pysize.btn_height
    radius: pysize.radius_m

    property alias text: _text.text

    LKText {
        id: _text
        anchors.centerIn: parent
    }

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = Qt.binding(() => {
                return _text.contentWidth + pysize.padding * 2
            })
        }
    }
}
