import QtQuick 2.15
import ".."

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property Component delegate
    property bool      demoMode: false
    property string    progColorFg: pycolor.progress_fg
    property alias     progItem: _loader.item
    property real      progValue
    property int       progWidth: 0
    property alias     textItem: _text
    property int       __spacing: pysize.spacing_l

    Loader {
        id: _loader
        anchors.verticalCenter: parent.verticalCenter
        width: root.progWidth
        sourceComponent: root.delegate
        onLoaded: {
            this.item.demoMode = Qt.binding(() => root.demoMode)
            this.item.progColorFg = Qt.binding(() => root.progColorFg)
            root.progValue = Qt.binding(() => this.item.__progValue)
        }
        Component.onCompleted: {
            if (root.progWidth == 0) {
                root.progWidth = Qt.binding(() => {
                    return root.width - _text.contentWidth - root.__spacing
                })
            }
        }
    }

    LKText {
        id: _text
        anchors {
            left: _loader.right
            right: parent.right
            verticalCenter: parent.verticalCenter
            leftMargin: root.__spacing
        }
        clip: true
        elide: Text.ElideRight
    }
}
