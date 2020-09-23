import QtQuick 2.14
import "./LCButtons"

LCListView {

    property var p_childrenProps: Object()
    property var p_default: Array()
    property var r_checked: Array()
    property var r_data: Object()
    property var r_unchecked: Array()
    // extend props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      p_spacing
    //      r_count
    //      r_currentItem

    function fn_clicked(i, item) {}

    p_delegate: LCCheckBox {
        id: _item
        checked: r_data[p_index] ? true : false
        p_text: modelData
        property int p_index: model.index
        onClicked: {
            r_data[p_index] = checked
            if (checked) {
                r_checked.push(p_index)
                r_unchecked = fn__remove(r_unchecked, p_index)
            } else {
                r_unchecked.push(p_index)
                r_checked = fn__remove(r_unchecked, p_index)
            }

            fn_clicked(p_index, _item)
        }

        Component.onCompleted: {
            for (let k in p_childrenProps) {
                _item[k] = p_childrenProps[k]
            }
        }
    }

    function fn__remove(arr, val) {
        // https://www.jianshu.com/p/b01363f88e64
        const pos = arr.indexOf(val)
        if (pos >= 0) {
            arr.splice(pos, 1)
        }
        return arr
    }

    Component.onCompleted: {
        for (let i in p_default) {
            r_data[p_default[i]] = true
            r_checked.push(p_default[i])
            r_unchecked = fn__remove(r_unchecked, p_default[i])
        }
    }
}