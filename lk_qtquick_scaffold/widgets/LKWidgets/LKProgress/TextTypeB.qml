import QtQuick 2.15
import ".."

LKText {
    id: root
    elide: Text.ElideRight

    property var model
    property var value

    Component.onCompleted: {
        this.modelChanged.connect(() => {
            this.maxText = pyside.eval(`
                return max(
                    map(str, model.values()),
                    key=len
                )
            `, {'model': this.model})
        })
        this.valueChanged.connect(() => {
            if (this.model) {
                this.text = lkprogress.get_nearest_value(
                    this.value, this.model
                )
            }
        })
    }
}
