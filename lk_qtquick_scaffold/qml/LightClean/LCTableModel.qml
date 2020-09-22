import QtQml.Models 2.14
import Qt.labs.qmlmodels 1.0

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

    property var p_header  // [str title, ...]
    property var p_model  // [{title: value}, ...]
}