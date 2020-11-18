import QtQuick 2.15
import "./LKStyle/dimension.js" as LKGeometry

Row {
    spacing: LKGeometry.HSpacingM

    property alias p_digitOnly: _edit.p_digitOnly
    property alias p_hint: _edit.p_hint
    property alias p_title: _edit.p_title
    property alias p_value: _edit.p_value

    property alias p_dialogTitle: _browse.p_dialogTitle
    property alias p_filetype: _browse.p_filetype
    property alias p_path: _browse.p_path
    property alias p_selectFolder: _browse.p_selectFolder
    property alias p_selectMultiple: _browse.p_selectMultiple

    LKEditField {
        id: _edit
        anchors.verticalCenter: parent.verticalCenter
        p_title: "Input"
    }

    LKFileBrowseButton {
        id: _browse
        anchors.verticalCenter: parent.verticalCenter
    }

    Component.onCompleted: {
        p_path = p_value
    }
}
