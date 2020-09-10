import QtQuick 2.15
import QtQuick.Controls 2.15
import "../Spec/palette.js" as Palette

Rectangle {
    id: _root
    border.color: Palette.BORDER_NORMAL
    border.width: _area.pressed ? 0 : 1
    color: _area.pressed ? Palette.BUTTON_PRESSED : Palette.BUTTON_NORMAL
    //implicitWidth: 60; implicitHeight: 20
    radius: 5

    property alias obj_MouseArea: _area
    property alias p_text: _txt.p_text
    //property alias __pressed: _area.pressed
    signal clicked()

    MyText {
        id: _txt
        anchors.centerIn: parent
        p_bold: true
        p_color: _area.pressed ? Palette.TEXT_WHITE : Palette.TEXT_NORMAL
        p_size: 13
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor  // i would like to use the pointing finger
        hoverEnabled: true
        onClicked: {
            _root.clicked()
        }
    }
}