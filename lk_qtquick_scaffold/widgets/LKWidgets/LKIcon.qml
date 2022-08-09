import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    // https://stackoverflow.com/questions/15236304/need-to-change-color-of
    //  -an-svg-image-in-qml
    id: root

    enabled: false
    background: Item {}
    flat: true
    hoverEnabled: false
    icon.width: root.size
    icon.height: root.size
    icon.color: root.color
    icon.source: root.source

    property string color
    property alias  hovered: _area.containsMouse
    property alias  icon: _btn.icon
    property int    size: pysize.icon_size
    property string source
}
