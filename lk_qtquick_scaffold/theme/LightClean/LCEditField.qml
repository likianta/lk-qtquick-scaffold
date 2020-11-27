import QtQuick 2.15
import "./LCStyle/dimension.js" as LCGeometry

Item {
    id: _root
    height: LCGeometry.BarHeight

    property alias p_digitOnly: _edit.p_digitOnly
    property alias p_hint: _edit.p_hint
    property alias p_title: _title.p_text
    property alias p_value: _edit.p_text

    signal clicked()

    // Title field
    LCText {
        id: _title
        anchors.right: _edit.left
        anchors.rightMargin: LCGeometry.MarginM
        height: parent.height
        horizontalAlignment: Text.AlignRight; verticalAlignment: Text.AlignVCenter
        p_bold: true
    }
    
    // Editbar
    LCEdit {
        id: _edit
        anchors.right: parent.right
        Component.onCompleted: {
            this.clicked.connect(_root.clicked)
        }
    }

    Component.onCompleted: {
        _root.width = childrenRect.width
    }
}
