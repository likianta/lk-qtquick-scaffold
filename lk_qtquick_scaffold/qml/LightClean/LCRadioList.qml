import "./LCButtons"

LCListView {
    id: _root

    property alias r_select: _root.p_currentIndex
    // extend props:
    //      p_currentIndex
    //      p_delegate
    //      p_model
    //      r_count
    //      r_currentItem

    function fn_clicked(i, item) {}

    p_delegate: LCRadioButton {
        id: _item
        p_text: modelData
        property int p_index: model.index
        onClicked: {
            p_currentIndex = p_index
            fn_clicked(p_index, _item)
        }
    }
}