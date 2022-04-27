import QtQuick

Column {
    width: pysize.col_width_m
    spacing: pysize.v_spacing_m

    property bool autoSize: true
    property bool centerAlignChildren: true

    Component.onCompleted: {
        if (this.centerAlignChildren) {
            for (let i = 0; i < this.children.length; i++) {
                this.children[i].anchors.horizontalCenter = Qt.binding(() => {
                    return this.horizontalCenter
                })
            }
        }
        if (this.autoSize) {
            pylayout.auto_size_children(this, pylayout.VERTICAL)
        }
    }
}
