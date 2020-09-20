import QtQuick 2.14
import QtQuick.Window 2.14

// https://qml.guide/live-reloading-hot-reloading-qml/+&cd=1&hl=zh-CN&ct=clnk&gl=sg
// https://stackoverflow.com/questions/58716153/how-to-force-loader-to-reload-reset-or-delete-the-cache-of-preloaded-qml-page
//  ^ this seems not work.

Window {
    visible: true
    width: 300; height: 120
    title: "Qml Hot Reloader"

    property string p_target: ""  // You must define the target to use.

    Text {
        anchors.centerIn: parent
        text: "Click to reload"
    }

    Loader {
        id: _loader
        anchors.centerIn: parent
        source: p_target

        function reload() {
            source = ""
            // QmlEngine.clearComponentCache()  // A: not work
            PyHandler.main('clearComponentCache')  // B
            source = p_target
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            _loader.reload()
        }
    }
}
