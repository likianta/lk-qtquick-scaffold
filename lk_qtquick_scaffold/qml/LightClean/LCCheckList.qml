import QtQuick 2.14
import "./LCButtons"

LCListView {

    property var p_childrenProps: Object()
    property var p_default: Array()
    property var r_checked: Array()
    property var r_checks: Object()
    property var r_unchecked: Array()
    // extend props:
    //      p_currentIndex
    //      p_delegate
    //      p_model  // [str, ...]
    //      p_spacing
    //      r_count
    //      r_currentItem

    function fn_clicked(i, item) {}

    p_delegate: LCCheckBox {
        id: _item
        p_text: modelData
        property int r_index: model.index
        onClicked: {
            fn__updateCheckState(_item)
            fn_clicked(r_index, _item)
        }

        Component.onCompleted: {
            for (let k in p_childrenProps) {
                _item[k] = p_childrenProps[k]
            }
            // console.log("LCCheckList.qml:34", r_checked)
            if (p_default.indexOf(_item.r_index) != -1) {
                _item.checked = true
            }
        }
    }

    function fn__updateCheckState(item) {
        r_checks[item.r_index] = item.checked
        if (item.checked) {
            if (r_checked.indexOf(item.r_index) == -1) {
                r_checked.push(item.r_index)
            }
            const pos = r_unchecked.indexOf(item.r_index)
            if (pos != -1) {
                r_unchecked.splice(pos, 1)
            }
        } else {
            if (r_unchecked.indexOf(item.r_index) == -1) {
                r_unchecked.push(item.r_index)
            }
            const pos = r_checked.indexOf(item.r_index)
            if (pos != -1) {
                r_checked.splice(pos, 1)
            }
        }
    }

    Component.onCompleted: {
        for (let i in p_default) {
            r_checks[p_default[i]] = true
            r_checked.push(p_default[i])
        }
        // console.log("LCCheckList.qml:67", r_checked)
    }
}