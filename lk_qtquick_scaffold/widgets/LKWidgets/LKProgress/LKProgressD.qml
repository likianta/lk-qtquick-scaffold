import QtQuick 2.15
import ".."

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property alias  demoMode: _prog.demoMode
    property alias  model: _prog.model
    property alias  progItem: _prog
    property alias  progValue: _prog.progValue
    property alias  progWidth: _prog.width
    property alias  textItem: _text

    LKProgressB {
        id: _prog
        anchors.verticalCenter: parent.verticalCenter
        width: 0
//        model: root.model
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
//            baseline: parent.verticalCenter
            verticalCenter: parent.verticalCenter
            verticalCenterOffset: -2
        }

        property alias __model: _prog.__model
        property alias __value: _prog.__progValue

        Component.onCompleted: {
            this.__valueChanged.connect(() => {
                if (this.__model) {
                    this.text = lkprogress.get_nearest_value(
                        this.__value, this.__model
                    )
                }
            })
            this.__modelChanged.connect(() => {
                const maxLen = pyside.eval(`
                    return max(map(len, map(str, model.values())))
                `, {'model': this.__model})
                this.width = maxLen * this.font.pixelSize
//                console.log(maxLen, this.width)
                this.__valueChanged()
            })
        }
    }
}
