import QtQuick

Image {
    id: root
    width: p_size
    height: p_size

//    property bool   p_circle: false
    property int    p_size: 0
    property alias  p_source: root.source
}