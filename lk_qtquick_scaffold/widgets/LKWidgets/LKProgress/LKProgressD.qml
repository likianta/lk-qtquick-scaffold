import QtQuick 2.15

ProgBaseCD {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property var  model
    property var  __model
    property real __value

    delegate: LKProgressB {
        model: root.model
        Component.onCompleted: {
            root.__model = Qt.binding(() => this.__model)
            root.__value = Qt.binding(() => this.__progValue)
        }
    }

    Component.onCompleted: {
        this.__valueChanged.connect(() => {
            if (this.model) {
                this.textItem.text = lkprogress.get_nearest_value(
                    this.__value, this.__model
                )
            }
        })
        this.__modelChanged.connect(() => {
            const maxLen = pyside.eval(`
                return max(map(len, map(str, model.values())))
            `, {'model': this.__model})
//            console.log(this.__model, maxLen)
            this.textItem.width = maxLen * this.textItem.font.pixelSize
//                console.log(maxLen, this.textItem.width)
            this.__valueChanged()
        })
    }
}
