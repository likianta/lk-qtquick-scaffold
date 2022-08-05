import QtQuick 2.15
import ".."

LKRectangle {
    id: _prog_fg
    anchors.left: parent.left
    width: parent.width * root.__progValue
    height: parent.height
//            radius: parent.radius
    color: root.progColorFg

    Behavior on width {
        enabled: root.demoMode
        NumberAnimation {
            duration: 200
        }
    }
}
