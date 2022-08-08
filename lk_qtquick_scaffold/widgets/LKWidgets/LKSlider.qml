import QtQuick 2.15
import "LKProgress"

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property var    model
    property string progColorFg: pycolor.progress_fg
    property alias  progItem: _prog_loader.item
    property real   progValue
    property int    progWidth: 0
    property bool   showText: true
    property string __progType: {  // literal['A', 'B', 'C', 'D']
        if (model) {
            if (showText) {
                return 'D'
            } else {
                return 'B'
            }
        } else {
            if (showText) {
                return 'C'
            } else {
                return 'A'
            }
        }
    }

    signal progItemLoaded(var progItem)
    signal progressChangedByUser(real value)

    Loader {
        id: _prog_loader
        anchors.fill: parent
        source: 'LKProgress/LKProgress' + root.__progType + '.qml'

        onLoaded: {
            switch (root.__progType) {
                case 'A':
                    break
                case 'B':
                    this.item.model = Qt.binding(() => root.model)
                    break
                case 'C':
                    this.item.progWidth = Qt.binding(() => root.progWidth)
                    break
                case 'D':
                    this.item.model = Qt.binding(() => root.model)
                    this.item.progWidth = Qt.binding(() => root.progWidth)
                    break
            }

            if (root.progWidth == 0) {
                if (root.showText) {
                    root.progWidth = Qt.binding(() => {
                        return root.width
                            - this.item.textItem.contentWidth
                            - pysize.spacing_l
                    })
                } else {
                    root.progWidth = Qt.binding(() => root.width)
                }
            }

            this.item.progColorFg = Qt.binding(() => root.progColorFg)
            this.item.progValue = Qt.binding(() => root.progValue)
            root.progItemLoaded(this.item)
        }
    }

    Item {
        id: _invisible_draggee
    }

    MouseArea {
        anchors.fill: parent
        drag.target: _invisible_draggee

        property alias __progItem: _prog_loader.item

        function __updateProgress(x) {
            root.progValue = x / this.__progItem.progWidth
            root.progressChangedByUser(this.__progItem.__progValue)
        }

        onClicked: (mouse) => {
            __updateProgress(mouse.x)
        }

        onPositionChanged: (mouse) => {
            if (this.drag.active) {
                __updateProgress(mouse.x)
            }
        }
    }
}
