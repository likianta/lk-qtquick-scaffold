import QtQuick

Rectangle {
    id: root
    width: 0
    height: pysize.button_height
    radius: pysize.radius_m
//    color: pycolor.white

    border.width: pysize.border_width_m
//    border.width: pressed ? pysize.border_width_l : pysize.border_width_m
    border.color: hovered ? pycolor.border_active : pycolor.border_default
    color:
        pressed ? pycolor.button_pressed :
        hovered ? pycolor.button_hovered : pycolor.button_default

    property alias hovered: _area.containsMouse
    property alias pressed: _area.pressed
    property alias text: _text.text
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
    }

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = Qt.binding(() => {
                return _text.contentWidth * 1.5
            })
        }
    }
}
