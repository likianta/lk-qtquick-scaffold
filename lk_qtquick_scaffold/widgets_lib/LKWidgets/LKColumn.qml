import QtQuick 2.15

Column {
    width: pysize.col_width_m
    spacing: pysize.v_spacing_m

    property string alignment: 'hcenter,hfill'
    property bool   autoSize: false

    Component.onCompleted: {
        if (this.alignment) {
            pylayout.auto_align(this, this.alignment)
        }
        if (this.autoSize) {
            pylayout.auto_size_children(this, pylayout.VERTICAL)
        }
    }
}
