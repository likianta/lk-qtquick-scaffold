import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension

LCRow {
    height: LCDimension.BarHeight

    property alias p_hint: _edit.p_hint
    property alias p_title: _title.p_text
    property alias p_value: _edit.p_text

    signal clicked()

    // Title field
    LCText {
        id: _title
        height: parent.height
        p_alignment: 'rcenter'
    }
    
    // Editbar
    LCEdit {
        id: _edit
        width: parent.width - _title.width
        p_alignment: 'lcenter'

        Component.onCompleted: {
            this.clicked.connect(parent.clicked)
        }
    }

    Component.onCompleted: {
        this.width = childrenRect.width
    }
}
