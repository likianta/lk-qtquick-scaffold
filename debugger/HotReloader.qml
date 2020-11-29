import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

/* 
    References:
        https://qml.guide/live-reloading-hot-reloading-qml/+&cd=1&hl=zh-CN&ct
        =clnk&gl=sg
        https://stackoverflow.com/questions/58716153/how-to-force-loader-to
        -reload-reset-or-delete-the-cache-of-preloaded-qml-page
        (↑ This seems not work.)
 */

Window {
    color: '#f2f2f2'
    flags: Qt.WindowStaysOnTopHint
    title: "Hot Reloader"
    visible: true
    // width: 300; height: 120
    width: _btn.width; height: _btn.height
    x: 1500; y: 400  // Appeared on the desktop left-vcenter.

    property string p_target: PyHandler.call('get_target')

    Loader {
        id: _loader
        anchors.centerIn: parent

        function reload() {
            source = ""
            console.log('------------------- Reload Target -------------------')
            // See `debugger.main.launch`
            PyHandler.call('clear_component_cache')
            this.source = p_target  // This will open a new window to show the
            //      target. (Cuz the target usually has a root Window widget
            //      itself)
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
            // border.width: 1; border.color: '#cccccc'
            color: {
                if (_btn.pressed) {
                    return '#4285f4'
                } else if (_btn.hovered) {
                    return '#ffffff'
                } else {
                    return '#f2f2f2'
                }
            }
            // radius: 12
        }

        contentItem: Text {
            font.pixelSize: 28
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: _btn.text
        }

        onClicked: _loader.reload()
    }
}
