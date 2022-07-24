import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    // https://stackoverflow.com/questions/15236304/need-to-change-color-of-an
    //  -svg-image-in-qml
    enabled: false
    width: size
    height: size
    background: Item {}
    flat: true
    icon.width: width
    icon.height: height
    icon.color: color
    icon.source: source

//    property alias color: icon.color
//    property alias  source: icon.source
    property string color
    property int    size: pysize.icon_size
    property string source
}
