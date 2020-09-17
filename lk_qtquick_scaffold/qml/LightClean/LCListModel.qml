import QtQml.Models 2.14

ListModel {
    id: _model
    /*  REF: https://forum.qt.io/topic/110659/q_arg-missing-in-python-how-to
     *      -use-invokemethod+&cd=2&hl=zh-CN&ct=clnk&gl=sg
     *  See also: pycomm.QtHooks.update_list_model()
     */
    property var py_newData  // js dict
    function pyAppend() {
        _model.append(py_newData)
    }

    // function pyClear() {
    //     _model.clear()
    // }
}
