import QtQuick 2.15
import ".."

LKText {
    id: root
    elide: Text.ElideRight

    property bool demoMode: false
    property int  precision: 0  // suggested 0 or 2
    property real value

    Behavior on value {
        NumberAnimation {
            duration: root.demoMode ? 500 : 100
        }
    }

    Component.onCompleted: {
        this.maxText = lkprogress.show_value(1.0, this.precision)
        this.valueChanged.connect(() => {
            this.text = lkprogress.show_value(
                this.value, this.precision
            )
        })
//        this.valueChanged()
    }
}
