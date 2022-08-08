import QtQuick 2.15
import ".."

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property alias  demoMode: _prog.demoMode
    property int    precision: 0  // suggested 0 or 2
    property alias  progItem: _prog
    property alias  progValue: _prog.progValue
    property alias  progWidth: _prog.width
    property alias  textItem: _text

    LKProgressA {
        id: _prog
        anchors.verticalCenter: parent.verticalCenter
        width: 0
        Component.onCompleted: {
            if (this.width == 0) {
                this.anchors.left = Qt.binding(() => root.left)
                this.anchors.right = Qt.binding(() => _text.left)
                this.anchors.rightMargin = pysize.spacing_l
            }
        }
    }

    LKText {
        id: _text
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }

        property real __value: _prog.__progValue

        Behavior on __value {
            NumberAnimation {
                duration: root.demoMode ? 500 : 100
            }
        }

        Component.onCompleted: {
            this.text = lkprogress.show_value(100, root.precision)
            this.width = this.contentWidth
            this.__valueChanged.connect(() => {
                this.text = lkprogress.show_value(
                    this.__value, root.precision
                )
            })
            this.__valueChanged()
        }
    }
}
