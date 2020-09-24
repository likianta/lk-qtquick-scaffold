import QtQuick 2.14
import "./LCButtons"

LCListView {

    property var p_childrenProps: Object()
    property var p_default: Array()
    property var r_checked: Set()
    property var r_checks: Object()
    property var r_unchecked: Set()
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
            fn__updateCheckState(_item)
            fn_clicked(p_index, _item)
        }

        Component.onCompleted: {
            for (let k in p_childrenProps) {
                _item[k] = p_childrenProps[k]
            }
            fn__updateCheckState(_item)
        }
    }

    function fn__updateCheckState(item) {
        r_data[item.p_index] = item.checked
        if (item.checked) {
            r_checked.add(item.p_index)
            r_unchecked.delete(item.p_index)
        } else {
            r_checked.delete(item.p_index)
            r_unchecked.add(item.p_index)
        }
    }

    Component.onCompleted: {
        for (let i in p_default) {
            r_data[p_default[i]] = true
            r_checked.add(p_default[i])
        }
    }
}