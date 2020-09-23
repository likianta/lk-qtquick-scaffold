import "./LCButtons"

LCListView {

    property var r_checked: Array()
    // extend props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      r_count
    //      r_currentItem

    function fn_clicked(i, item) {}

    p_delegate: LCCheckBox {
        id: _item
        checked: r_checked[p_index] ? true : false
        p_text: modelData
        property int p_index: model.index
        onClicked: {
            r_checked[p_index] = checked
            fn_clicked(p_index, _item)
        }
    }
}