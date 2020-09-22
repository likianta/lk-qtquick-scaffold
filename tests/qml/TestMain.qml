import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.14
import LightClean 1.0
import LightClean.LCButtons 1.0
import Qt.labs.qmlmodels 1.0
import QtQml.Models 2.14

Window {
    id: _root
    // color: "#F2F2F2"
    visible: true
    width: 800; height: 600

    LCTable {
        id: _table
        //anchors.centerIn: parent
        // width: 500; height: 300
        width: 500; height: 200
        // anchors.fill: parent

        p_header: ["aaa", "bbb", "ccc", 'ddd', 'eee']
        p_model: [
            {"aaa": "alpha", "bbb": "beta", 'ccc': 'cyan', 'ddd': 'dele', 'eee': 'ele'},
            {"aaa": "asdfasdf", "bbb": "baaetr2342342342341455dsfasfdasdfrt", 'ccc': 'cqwerq', 'ddd': 'daweraf', 'eee': 'eafh'},
        ]
        Component.onCompleted: {
            console.log("tests/qml/TestMain.qml:26", _table.width, _table.contentWidth)
        }
    }

    LCButton {
        anchors.top: _table.bottom
        p_text: "Check size"
        onClicked: {
            console.log("tests/qml/TestMain.qml:36",
                        _table.width, _table.contentWidth, _table.height, _table.contentHeight)
        }
    }
}
