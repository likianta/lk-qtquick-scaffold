import QtQuick

Row {
    spacing: pysize.spacing_m
    property bool centerAlignChildren: true
    Component.onCompleted: {
        if (this.centerAlignChildren) {
            for (let i = 0; i < this.children.length; i++) {
                this.children[i].anchors.verticalCenter = Qt.binding(() => {
                    return this.verticalCenter
                })
            }
        }
    }
}
