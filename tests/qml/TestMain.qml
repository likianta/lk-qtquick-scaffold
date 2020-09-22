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
        //anchors.centerIn: parent
        width: 500; height: 300

        p_header: ["aaa", "bbb"]
        p_model: [
            {"aaa": "alpha", "bbb": "beta"},
            {"aaa": "asdfasdf", "bbb": "baaetrrt"},
        ]
    }
}
