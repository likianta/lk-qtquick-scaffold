import QtQuick
import QtQuick.Controls
import QtQuick.Window

//  References:
//      https://qml.guide/live-reloading-hot-reloading-qml

Window {
    color: '#f2f2f2'
    flags: Qt.WindowStaysOnTopHint
    title: "Hot Reloader"
    visible: true
    width: _btn.width; height: _btn.height
    //  width: 300; height: 120
    x: 1200; y: 400  // appeared on the desktop left-vcenter.

    property int    p_cnt: -1
    property string p_target: pyside.call('__get_target_to_load')

    Loader {
        id: _loader
        anchors.centerIn: parent

        function reload() {
            p_cnt += 1
            console.log(
                `================= Reload Target (${p_cnt}) =================`
            )

            source = ""
            pyside.call('__clear_component_cache')
            _loader.source = p_target
            //  this will open a new window to show the target. (because the
            //  target usually has a root Window widget itself.)
        }
    }

    Button {
        id: _btn
        anchors.centerIn: parent
        hoverEnabled: true
        text: "Reload"
        width: 200; height: 100

        background: Rectangle {
            id: _rect
            color: {
                if (_btn.pressed) {
                    return '#4285f4'
                } else if (_btn.hovered) {
                    return '#ffffff'
                } else {
                    return '#f2f2f2'
                }
            }
        }

        contentItem: Text {
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: _btn.text
        }

        onClicked: _loader.reload()
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
        console.log('HotLoader started!')
    }
}
