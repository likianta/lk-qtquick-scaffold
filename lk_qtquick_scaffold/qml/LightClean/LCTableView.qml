import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.14
import Qt.labs.qmlmodels 1.0
import "./LCStyle/geometry.js" as LCGeometry

// DELETE: This component is going to be removed. Please refer to LCTable.
// https://blog.csdn.net/qq_43627981/article/details/106424736
// https://doc.qt.io/qt-5/qml-qt-labs-qmlmodels-tablemodel.html+&cd=2&hl=zh-CN&ct=clnk&gl=sg

TableView {
    id: _root
    clip: true
    model: _model

    property alias i_model: _model
    property alias p_delegate: _root.delegate
    property var p_header  // [str title, ...]
    property var p_model  // [{title: value}, ...]

    Component {
        id: _model
        TableModel {
            /*
                You should define TableModelColumn manually, and cannot use
                    Repeater on it, because Repeater will raise an error:
                    'Cannot assign object to list property "columns"'.
                E.g.
                    LCTableView {
                        i_model {
                            // Manually set the TableModelColumn.
                            TableModelColumn { display: title1 }
                            TableModelColumn { display: title2 }
                            TableModelColumn { display: title3 }
                            //      The titles are `p_model[0].keys()`.
                            ...
                            rows: p_model  // p_model: [{title: value}, ...]
                        }
                    }
             */
            rows: p_model
        }
    }
}