import QtQuick 2.15
import QtQuick.Dialogs 1.3
import "./LCButtons"

LCButton {
    p_text: "Browse"

    property alias  p_dialogTitle: _dialog.title
    property alias  p_filetype: _dialog.nameFilters  // [str, ...]
    /*      Examples:
                ["All files (*.*)"]
                ["Excel file (*.xlsx *.xls)"]
                ["PDF file (*.pdf)"]
                ["Plain file (*.txt *.md *.rst *.json *.ini)"]
                ["Text file (*.txt)"]
     */
    property string p_path
    property alias  p_selectFolder: _dialog.selectFolder
    property alias  p_selectMultiple: _dialog.selectMultiple

    onClicked: _dialog.open()

    FileDialog {
        id: _dialog
        // folder: shortcuts.desktop
        selectExisting: true
        selectFolder: false
        selectMultiple: false
        title: "File dialog"

        onAccepted: {
            // Note that `this.fileUrl` is typeof Object, not string. We should
            // convert it to string before we assign it to `p_path`.
            // Use `fileUrl + ""` to convert it to string, the value is like
            // 'file:///d:/...', slice out 'file:///' then pass it to `p_path`.
            p_path = (this.fileUrl + "").slice(8)
        }
    }
}
