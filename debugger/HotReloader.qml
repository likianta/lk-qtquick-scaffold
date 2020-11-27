import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

/* 
    References:
        https://qml.guide/live-reloading-hot-reloading-qml/+&cd=1&hl=zh-CN&ct=clnk&gl=sg
        https://stackoverflow.com/questions/58716153/how-to-force-loader-to-reload-reset-or-delete-the-cache-of-preloaded-qml-page 
        (↑ This seems not work.)
 */

Window {
    color: '#f2f2f2'
    visible: true
    // width: 300; height: 120
    width: _btn.width; height: _btn.height
    title: "Hot Reloader"

    property string p_target: ""

    Loader {
        id: _loader
        anchors.centerIn: parent

        function reload() {
            source = ""
            // See `debugger.main.py:19`
            PyHandler.main('clearComponentCache')  
            source = p_target  // This will open a new window to show the target
            //  (cause the target usually has a root Window widget itself).
        }
    }

    Button {
        id: _btn
        anchors.centerIn: parent
        text: "Reload"
        width: 200; height: 80

        background: Rectangle {
            border.width: 1; border.color: '#cccccc'
            color: _btn.pressed ? '#4285f4' : 'white'
            // radius: 12
        }

        contentItem: Text {
            font.family: 'Microsoft YaHei'
            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
            text: _btn.text
        }

        onClicked: _loader.reload()
    }
}
