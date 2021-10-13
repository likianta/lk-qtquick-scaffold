import QtQuick
import QtQuick.Controls

LCRectangle {
    id: root
    width: 220
    height: 32
    color: '#eeeeee'

    property alias p_field: txt.text
    property int   p_index: 0
    property alias p_values: combox.model

    LCText {
        id: txt
        anchors.left: parent.left
        anchors.leftMargin: 12
        anchors.verticalCenter: parent.verticalCenter
    }

    ComboBox {
        id: combox
        anchors.right: parent.right
        anchors.rightMargin: 6
        anchors.verticalCenter: parent.verticalCenter
        width: 72
        height: 24

        background: LCRectangle {
            border.width: 1
            border.color: '#0984d8'
            color: '#ffffff'
            radius: root.radius
        }

        contentItem: LCText {
            text: combox.displayText
            p_bold: true
            p_size: 11
        }

        Component.onCompleted: {


        }
    }
}
