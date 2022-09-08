import QtQuick 2.15

Item {
    id: root
    property string color: pycolor.progress_fg
    property alias  radius: _rect.radius
    property real   value: 0  // 0.0 ~ 1.0
    Rectangle {
        id: _rect
        width: parent.width * parent.value
        height: parent.height
        radius: pysize.progress_radius
        color: parent.color
    }
}
