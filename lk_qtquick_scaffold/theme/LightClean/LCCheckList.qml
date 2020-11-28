import QtQuick 2.15
import "./LCButtons"

LCListView {
    id: _root

    property var p_checks: Object()  // {index: bool, ...}
    property var p_childrenProps: Object()
    // inherits props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      p_spacing
    //      r_count
    //      r_currentItem

    signal clicked(int index, var checkbox)

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

    function getCheckStates() {  // -> {index: bool, ...}
        return p_checks
    }

    function __get(obj, key, default_val) {
        /*  Inplement Python's `dict.get(key, default)` in Javascript.

            References:
                https://stackoverflow.com/questions/44184794/what-is-the-javascript-equivalent-of-pythons-get-method-for
                -dictionaries
         */
        const result = obj[key]
        if (typeof result !== 'undefined') {
            return result
        } else {
            return default_val
        }
    }

    p_delegate: LCCheckBox {
        p_text: modelData

        property int r_index: model.index

        onClicked: {
            _root.p_checks[this.r_index] = this.checked
            _root.clicked(this.r_index, this)
        }

        Component.onCompleted: {
            this.checked = __get(p_checks, model.index, false)
            for (let k in p_childrenProps) {
                this[k] = p_childrenProps[k]
            }
        }
    }
}
