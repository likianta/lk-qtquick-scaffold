import QtQuick 2.15

Item {
    id: root

    property real demoValue
    property int  progWidth

    Item {
        id: _invisible_draggee
    }

    MouseArea {
        anchors.fill: parent
        drag.target: _invisible_draggee
        onClicked: (mouse) => {
            root.demoValue = mouse.x / root.progWidth
//            console.log(mouse.x, root.demoValue)
        }
        onPositionChanged: (mouse) => {
            if (this.drag.active) {
                root.demoValue = mouse.x / root.progWidth
            }
        }
    }
}
