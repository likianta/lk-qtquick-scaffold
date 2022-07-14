import QtQuick 2.15
import QtQuick.Window 2.15

//  References:
//      https://qml.guide/live-reloading-hot-reloading-qml

Window {
    visible: true
    color: '#f2f2f2'
    flags: Qt.WindowStaysOnTopHint
    title: "Hot Reloader"

    Loader {
        id: _loader
        anchors.centerIn: parent
        Component.onCompleted: {
            PyHotLoaderControl.set_loader(this)
        }
    }

    Rectangle {
        id: _btn
        anchors.centerIn: parent
        width: 160
        height: 60

        Text {
            anchors.centerIn: parent
            color: _area.containsMouse ? '#5f00ff' : '#666666'
            font.pixelSize: 28
            text: 'Reload'
//            Behavior on color {
//                ColorAnimation {
//                    duration: 100
//                }
//            }
        }

        MouseArea {
            id: _area
            anchors.fill: parent
            hoverEnabled: true
            onClicked: PyHotLoaderControl.reload()
        }

        Component.onCompleted: {
            this.color = PyHotLoaderControl.get_bg_color()
        }
    }

    // Rectangle {
    //     id: _tip
    //     // anchors.verticalCenter: parent.verticalCenter
    //     // anchors.rightMargin: 20
    //     anchors.right: parent.right
    //     anchors.bottom: parent.bottom
    //     anchors.margins: 6
    //     width: 12; height: 12; radius: 6
    //     color: '#38de8d'
    //
    //     MouseArea {
    //         id: _area
    //         anchors.fill: parent
    //         hoverEnabled: true
    //     }
    // }

    Component.onCompleted: {
        this.width = _btn.width
        this.height = _btn.height
        // move window to right-center.
        const scr_width = Screen.width
        const scr_height = Screen.height
        this.x = scr_width - 200 - this.width
        this.y = scr_height / 2 - this.height / 2
        this.visible = true
        console.log(`HotLoader started! (position at [${this.x}, ${this.y}])`)
    }
}
