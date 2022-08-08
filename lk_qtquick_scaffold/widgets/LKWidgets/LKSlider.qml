import QtQuick 2.15
import "LKProgress"

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property var    model
    property real   progValue
    property bool   showText
    property string __progType: {  // 'A' | 'B' | 'C' | 'D'
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

    signal progressChangedByUser(real value)
//    signal __loaded(var progItem)

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
                    break
                case 'D':
                    this.item.model = Qt.binding(() => root.model)
                    break
            }
            this.item.progValue = Qt.binding(() => root.progValue)
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
