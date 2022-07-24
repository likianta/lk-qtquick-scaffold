import QtQuick 2.15
import ".."

Rectangle {
    id: root
    width: 0
    height: pysize.button_height
    radius: pysize.button_radius
    border.width: pysize.border_width_m
//    border.width: pressed ? 2 : 1
    border.color: hovered ? pycolor.border_active : pycolor.border_default
//    color: pycolor.white
    color:
        pressed ? pycolor.button_bg_pressed :
        hovered ? pycolor.button_bg_hovered : pycolor.button_bg_default

    property alias  hovered: _area.containsMouse
    property alias  pressed: _area.pressed
    property string text
    property alias  textDelegate: _text

    signal clicked()

    Behavior on border.color {
        enabled: root.border.width > 0
        ColorAnimation {
            duration: pymotion.duration_m
        }
    }

    LKMouseArea {
        id: _area
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }

    LKText {
        id: _text
        anchors.centerIn: parent
        text: root.text
    }

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = Qt.binding(() => {
                return _text.contentWidth * 1.5
            })
        }
    }
}
