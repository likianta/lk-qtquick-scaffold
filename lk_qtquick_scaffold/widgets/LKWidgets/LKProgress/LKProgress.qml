import QtQuick 2.15

Loader {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property bool   demoMode: false
    property var    model
    property int    precision: 0  // suggested 0 or 2
//    property string progColorBg: pycolor.progress_bg
    property string progColorFg: pycolor.progress_fg
    property int    progWidth: 0
    property bool   showText: false
    property var    textItem

    onLoaded: {
        this.item.demoMode = Qt.binding(() => this.demoMode)
        this.item.progColorFg = Qt.binding(() => this.progColorFg)

        if (this.model) {
            this.item.model = Qt.binding(() => this.model)
        } else {
            if (this.showText) {
                this.item.precision = Qt.binding(() => this.precision)
            }
        }

        if (this.showText) {
            this.item.progWidth = Qt.binding(() => this.progWidth)
            this.textItem = Qt.binding(() => this.item.textItem)
        }
    }

    Component.onCompleted: {
        this.source = Qt.binding(() => {
            if (this.model) {
                if (this.showText) {
                    return pyassets.get(
                        'lkwidgets', 'LKWidgets/LKProgress/LKProgressB2.qml'
                    )
                } else {
                    return pyassets.get(
                        'lkwidgets', 'LKWidgets/LKProgress/LKProgressB.qml'
                    )
                }
            } else {
                if (this.showText) {
                    return pyassets.get(
                        'lkwidgets', 'LKWidgets/LKProgress/LKProgressA2.qml'
                    )
                } else {
                    return pyassets.get(
                        'lkwidgets', 'LKWidgets/LKProgress/LKProgressA.qml'
                    )
                }
            }
        })
    }
}
