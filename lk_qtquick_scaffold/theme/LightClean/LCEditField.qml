import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension

LCRow {
    id: root
    width: LCDimension.BarWidth
    height: LCDimension.BarHeight
    p_autoWidth: true
    p_fillHeight: true

    property alias p_hint: _edit.p_hint
    property alias p_title: _title.p_text
    property alias p_value: _edit.p_text

    signal clicked()

    // Title field
    LCText {
        id: _title
        p_alignment: 'rcenter'
    }
    
    // Editbar
    LCEdit {
        id: _edit
        width: 0
        p_alignment: 'lcenter'

        Component.onCompleted: {
            this.clicked.connect(parent.clicked)
        }
    }
}
