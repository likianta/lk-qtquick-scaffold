import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    width: size
    height: size
    clip: false

    property string color
    property alias  hovered: _area.containsMouse
    property alias  icon: _btn.icon
    property int    size: pysize.icon_size
    property string source

    signal clicked(var mouse)

    Button {
        // https://stackoverflow.com/questions/15236304/need-to-change-color-of
        //  -an-svg-image-in-qml
        id: _btn
        enabled: false
        anchors.centerIn: parent
        background: Item {}
        flat: true
        hoverEnabled: false
        icon.width: root.size
        icon.height: root.size
        icon.color: root.color
        icon.source: root.source
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: (mouse) => root.clicked(mouse)
    }
}
