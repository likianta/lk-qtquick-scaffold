import QtQuick
import LKWidgets

LKWindow {
    height: 120

    LKRow {
        id: _row
        anchors {
            left: parent.left
            right: parent.right
            verticalCenter: parent.verticalCenter
            margins: 24
        }
        height: 30
        clip: true

        component MyItem: LKRectangle {
            objectName: 'my_item_' + index
            height: _row.height

            property int  index

            LKText {
                anchors.centerIn: parent
                color: 'white'
                text: `[${parent.index}] ${parent.width}`
            }
        }

        MyItem {
            index: 0
            height: parent.height
            color: '#251CA3'
        }

        MyItem {
            index: 1
            width: 0.5
            height: parent.height
            color: '#F82184'
        }

        MyItem {
            width: 0.3
            height: parent.height
            color: '#43692A'
            index: 2
        }

        MyItem {
            id: _fixed_item
            width: 120
            height: parent.height
            color: '#239EA5'
            index: 3
        }
    }
}
