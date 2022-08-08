import QtQuick 2.15

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property bool      demoMode: false
    property alias     progBgItem: _prog_bg
    property Component progFgDelegate
    property Component progFgItem: _prog_fg_loader.item
    property string    progColorBg: pycolor.progress_bg
    property string    progColorFg: pycolor.progress_fg
    property real      progValue: 0  // usually 0.0 ~ 1.0, allow overflows.
    property real      __progValue  // 0.0 ~ 1.0

    ProgBg {
        id: _prog_bg
        anchors.centerIn: parent
        width: parent.width
        height: pysize.progress_height
        color: root.progColorBg

        Loader {
            id: _prog_fg_loader
            anchors.fill: parent
            sourceComponent: root.progFgItem
            onLoaded: {
                this.item.color = Qt.binding(() => root.progColorFg)
                this.item.value = Qt.binding(() => root.__progValue)
            }
        }
    }
}
