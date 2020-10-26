/*
    功能:
        减少 QML 布局代码的书写量.

    示例:
        import QtQuick 2.15
        import "~/js/layout-helper.js" as LayoutHelper
        Column {
            id: _col
            Component.onCompleted: {
                LayoutHelper.children_size(
                    _col.width - _col.padding * 2, 20
                )
            }
        }
 */

function childrenAlignment(parent, align) {
    // :param align: str, |'left', 'top', 'right', 'bottom', 'hcenter',
    //  'vcenter', 'center', 'left-top', 'left-bottom', 'top-left', 'top-right',
    //  'right-top', 'right-bottom', ...|
    if (align.indexOf("-") != -1) {

    } else {
        align = {
            "left": 0,
        }
    }
    childrenProps(parent, align)
}

function childrenSize(width, height) {
    // pass
}

function childrenProps(parent, props) {
    // props: {prop: value}
    for (let i in parent.children) {
        let child = parent.children[i]
        for (let prop in props) {
            let value = props[prop]
            child[prop] = value
        }
    }
}
