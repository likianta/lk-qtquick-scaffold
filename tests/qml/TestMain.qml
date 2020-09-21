import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.14
import LightClean 1.0

Window {
    id: _root
    // color: "#F2F2F2"
    visible: true
    width: 800; height: 370

    LCColumn {
        id: _row
        anchors.fill: parent
        width: 400
        height: 0

        LCRow {
            height: 30
            LCFileBrowse {
                id: _browse1
                width: 380; height: 30
                p_dialogTitle: "Select testcase excel"
                p_filetype: "excel"
                p_title: "Input excel"
                p_value: "../model/testcase.xlsx"
            }

        }

        LCRow {
            height: 200
            Layout.alignment: Qt.AlignTop
            LCFileBrowse {
                id: _browse2
                width: 380; height: 30
                p_dialogTitle: "Select testcase excel"
                p_filetype: "excel"
                p_title: "Input excel"
                p_value: "../model/testcase.xlsx"
            }

        }

        LCButton {
            id: _load
            objectName: "testcase_viewer/layout/FileBrowse.qml#_load"
            width: 80; height: 30
            p_autoSize: false
            p_text: "Load"
            onClicked: {
                i_overview.fn_updateConditions(
                    PyHandler.main("load", _browse.p_path)
                )
            }
        }
    }
}
