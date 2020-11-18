import QtQuick 2.15
import "./LKButtons/LKCheckBox.qml" as LKCheckBox

LKListView {
    id: _root
    property var p_childrenProps: Object()
    property var p_checks: Object()  // {index: bool, ...}
    // inherits props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      p_spacing
    //      r_count
    //      r_currentItem

    function fn_clicked(i, item) {}

    function getChecked() {  // -> [index, ...]
        let out = []
        for (var i in p_checks) {
            if (p_checks[i]) {
                out.push(i)
            }
        }
        return out
    }

    function getUnchecked() {  // -> [index, ...]
        let out = []
        for (var i in p_checks) {
            if (!p_checks[i]) {
                out.push(i)
            }
        }
        return out
    }

    function __get(obj, key, default_val) {
        // https://stackoverflow.com/questions/44184794/what-is-the-javascript-equivalent-of-pythons-get-method-for-dictionaries
        const result = obj[key]
        if (typeof result !== 'undefined') {
            return result
        } else {
            return default_val
        }
    }

    p_delegate: LKCheckBox {
        id: _item
        p_text: modelData
        property int r_index: model.index
        onClicked: {
            _root.p_checks[_item.r_index] = _item.checked
            fn_clicked(_item.r_index, _item)
        }

        Component.onCompleted: {
            _item.checked = __get(p_checks, model.index, false)
            for (let k in p_childrenProps) {
                _item[k] = p_childrenProps[k]
            }
        }
    }
}