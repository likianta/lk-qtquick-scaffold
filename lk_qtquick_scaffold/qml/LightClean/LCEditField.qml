import QtQuick 2.14
import "./Spec/geometry.js" as LCGeometry

Item {
    id: _root
    //width: childrenRect.width; height: LCGeometry.BarHeight
    height: LCGeometry.BarHeight

    property alias p_digitOnly: _edt.p_digitOnly
    property alias p_hint: _edt.p_hint
    property alias p_title: _title.p_text
    property alias p_value: _edt.p_text

    signal fn_clicked

    // Title field
    LCText {
        id: _title
        anchors.right: _edt.left
        anchors.rightMargin: LCGeometry.MarginM
        height: parent.height
        horizontalAlignment: Text.AlignRight; verticalAlignment: Text.AlignVCenter
        //width: parent.width - _edt.width; height: parent.height
        p_bold: true
    }
    
    // Editbar
    LCEdit {
        id: _edt
        anchors.right: parent.right
    }
}
