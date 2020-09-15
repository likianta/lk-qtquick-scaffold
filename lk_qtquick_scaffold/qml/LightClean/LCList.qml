import QtQuick 2.14
import QtQml.Models 2.14

Item {
    property alias obj_ListModel: _model
    property alias obj_ListView: _view

    ListModel {
        id: _model
        /*  REF: https://forum.qt.io/topic/110659/q_arg-missing-in-python-how-to
         *      -use-invokemethod+&cd=2&hl=zh-CN&ct=clnk&gl=sg
         *  See also: pycomm.QtHooks.update_list_model()
         */
        property var p_newData  // js dict
        function appendBridge() {
            _model.append(p_newData)
        }
    }

    ListView {
        id: _view
        model: _model
    }
}
