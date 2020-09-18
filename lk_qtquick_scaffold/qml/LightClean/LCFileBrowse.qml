import QtQuick 2.14
import QtQuick.Dialogs 1.3
import "./LCStyle/geometry.js" as LCGeometry

Row {
    property alias p_filetypes: _dialog.nameFilters  // e.g. ["Excel file (*.xlsx *.xls)"]
    property string p_path
    property alias p_selectFolder: _dialog.selectFolder
    property alias p_selectMultiple: _dialog.selectMultiple
    property alias p_title: _dialog.title

    LCEditField {
        id: _edit
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
    }

    FileDialog {
        id: _dialog
        anchors.left: _edit.right
        anchors.verticalCenter: parent.verticalCenter
        // heigth: _edit.height
        width: LCGeometry.ButtonWidth; height: LCGeometry.ButtonHeight

        selectExisting: true
        selectFolder: false
        selectMultiple: false
        title: "File dialog"

        onAccepted: {
            // Note that `fileUrl` is typeof Object, not string. We should
            //  convert it to string first.
            // Use `fileUrl + ""` to make it string, the value is
            //  'file:///d:/...', slice out 'file:///' then pass it to `p_path`.
            p_path = (fileUrl + "").slice(8)
        }
    }
}
