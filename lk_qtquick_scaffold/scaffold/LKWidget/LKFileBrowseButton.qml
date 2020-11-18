import QtQuick 2.15
import QtQuick.Dialogs 1.3
import "./LKButtons"
import "./LKStyle/dimension.js" as LKGeometry

LKButton {
    p_text: "Browse"

    property alias p_dialogTitle: _dialog.title
    property string p_filetype  // e.g. ["Excel file (*.xlsx *.xls)"]
    property string p_path
    property alias p_selectFolder: _dialog.selectFolder
    property alias p_selectMultiple: _dialog.selectMultiple

    property var __builtinFiletypes: {
        "all_files": ["All files (*.*)"],
        "excel": ["Excel file (*.xlsx *.xls)"],
        "pdf": ["PDF file (*.pdf)"],
        "txt": ["Text file (*.txt *.md *.rst *.json *.ini)"],
        ".txt": ["Text file (*.txt)"],
    }

    onClicked: _dialog.open()

    FileDialog {
        id: _dialog
        // folder: shortcuts.desktop
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

    Component.onCompleted: {
        const filetype = __builtinFiletypes[p_filetype]
        if (filetype == undefined) {
            _dialog.nameFilters = p_filetype
        } else {
            _dialog.nameFilters = filetype
        }
    }
}