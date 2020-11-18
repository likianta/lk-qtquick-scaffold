import "./LKStyle/palette.js" as LKPalette

LKRectangle {
    id: _root
    // when you need to put a field item, just define the property `p_key` & `p_val` in that item. LKForm will iterate
    //      these properties and post as a whole data.

    property var p_data: Object()

    // call `fn_collectData(_root)`
    function fn_collectData(rootItem) {
        for (let i in rootItem.children) {
            let child = rootItem.children[i]
            if (child.p_key) {
                p_data[child.p_key] = child.p_val
            } else {
                fn_collectData(child)  // function will finally return global variant `p_data`, but no need to receive it
                //      in recursive loops since it is global variant.
            }
        }
        return p_data
    }

    function fn_post(name) {
        return PyHandler.main(name, fn_collectData(_root))
    }
}