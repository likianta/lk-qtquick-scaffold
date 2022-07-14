/// the classic Rectangle-Text-MouseArea structure.
import QtQuick 2.15

LKRectangle2 {
    property alias text: _text
    property alias text_: _text.text
    LKText {
        id: _text
        anchors.centerIn: parent
    }
}
