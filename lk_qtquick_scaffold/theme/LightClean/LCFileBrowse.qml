import QtQuick 2.15
import QtQuick.Dialogs 1.3
import "./LCButtons"
import "./LCStyle/dimension.js" as LCDimension

LCEditField {
    id: root

    property alias  p_dialogTitle: _dialog.title
    property alias  p_filetype: _dialog.nameFilters  // [str, ...]
    /*      Examples:
                ["All files (*.*)"]
                ["Excel file (*.xlsx *.xls)"]
                ["PDF file (*.pdf)"]
                ["Plain file (*.txt *.md *.rst *.json *.ini)"]
                ["Text file (*.txt)"]
     */
    property alias  p_path: root.p_value
    property alias  p_selectFolder: _dialog.selectFolder
    property alias  p_selectMultiple: _dialog.selectMultiple
    // inherits:
    //      p_hint
    //      p_title
    //      p_value

    LCButton {
        id: _browseBtn
        p_text: "Browse"

        onClicked: _dialog.open()

        FileDialog {
            id: _dialog
            // folder: shortcuts.desktop
            selectExisting: true
            selectFolder: false
            selectMultiple: false
            title: "File dialog"

            onAccepted: {
                // Note that `this.fileUrl` is typeof Object, not string. We
                // should convert it to string before we assign it to `p_path`.
                // Use `fileUrl + ""` to convert it to string, the value is like
                // 'file:///d:/...', slice out 'file:///' then pass it to
                // `p_path`.
                root.p_path = (this.fileUrl + "").slice(8)
            }
        }
    }

    Component.onCompleted: {
        // Make the TextField (children[1])'s width adaptive.
        root.children[1].width = root.width -
                                 root.padding * 2 -
                                 root.spacing * 2 -
                                 root.children[0].width -
                                 root.children[2].width
    }
}
