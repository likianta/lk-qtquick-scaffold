import QtQuick 2.15
import "LKProgress"

LKProgress {
    id: root

    property bool draggable: true
    property int  draggableZone: indiRadius * 2
    property bool handCursorShape: true
    property int  indiRadius: 6

    // triggered when user drags the indicator.
    signal progressUpdatedByDragging(real prog)

    Item {
        id: _indicator
        anchors.verticalCenter: parent.verticalCenter
        x: root.progWidth * root.__progValue
        width: root.draggableZone
        height: root.draggableZone

        Behavior on x {
            enabled: root.demoMode
            NumberAnimation {
                duration: 200
            }
        }

        LKCircle {
            id: _real_indicator
            enabled: radius > 0
            anchors.verticalCenter: parent.verticalCenter
            x: -radius
            radius: root.indiRadius
            border.width: root.draggable ? 1 : 0
            border.color: 'white'
            color: root.progColorFg

            Behavior on radius {
                NumberAnimation {
                    duration: 100
                }
            }

            MouseArea {
                id: _indicator_area
                anchors.fill: parent
                hoverEnabled: true
            }

            Component.onCompleted: {
                root.__padding += this.radius
                root.draggableChanged.connect(() => {
                    if (root.draggable) {
                        this.radius = Qt.binding(() => root.indiRadius)
                    } else {
                        this.radius = 0
                    }
                })
            }
        }
    }

    Item {
        // just for activating drag.active` detection.
        id: _virtual_drag
    }

    MouseArea {
        enabled: !root.demoMode
        anchors.fill: parent
        drag.target: _virtual_drag

        function updateProgress(x) {
            if (x <= 0) {
                root.progValue = 0
            } else if (x >= root.progWidth) {
                root.progValue = 1
            } else {
                root.progValue = x / root.progWidth
            }
            root.progressUpdatedByDragging(root.progValue)
        }

        onClicked: (mouse) => {
            this.updateProgress(mouse.x)
        }

        onPositionChanged: (mouse) => {
            if (this.containsPress) {
                this.updateProgress(mouse.x)
            }
        }

//        onReleased: (mouse) => {
//            if (root.model) {
//                root.progValue = lkprogress.get_nearest_progress(
//                    mouse.x / root.progWidth, root.model
//                )
//            }
//        }

        Component.onCompleted: {
            if (root.handCursorShape) {
                this.cursorShape = Qt.binding(() => {
                    if (this.drag.active) {
                        return Qt.ClosedHandCursor
                    } else if (this.containsMouse) {
                        return Qt.OpenHandCursor
                    } else {
                        return Qt.ArrowCursor
                    }
                })
            }
        }
    }

    Component.onCompleted: {
        root.demoModeChanged.connect(() => {
            if (root.demoMode) {
                root.textClicked.connect(() => {
                    root.draggable = !root.draggable
                })
            }
        })
        if (root.demoMode) {
            root.demoModeChanged()
        }
    }
}
