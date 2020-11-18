import QtQuick 2.15
import "./LKStyle/dimension.js" as LKGeometry

Item {
    id: _root
    height: LKGeometry.BarHeight

    property alias p_digitOnly: _edit.p_digitOnly
    property alias p_hint: _edit.p_hint
    property alias p_title: _title.p_text
    property alias p_value: _edit.p_text

    signal fn_clicked

    // Title field
    LKText {
        id: _title
        anchors.right: _edit.left
        anchors.rightMargin: LKGeometry.MarginM
        height: parent.height
        horizontalAlignment: Text.AlignRight; verticalAlignment: Text.AlignVCenter
        p_bold: true
    }
    
    // Editbar
    LKEdit {
        id: _edit
        anchors.right: parent.right
    }

    Component.onCompleted: {
        _root.width = childrenRect.width
    }
}
