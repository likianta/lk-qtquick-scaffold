import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension

Row {
    id: root
    width: LCDimension.BarWidth
    height: LCDimension.BarHeight
    padding: LCDimension.Padding
    spacing: LCDimension.HSpacingM

    property bool  p_alignCenter: true
    property bool  p_autoWidth: false
    property bool  p_fillHeight: false
    property alias p_padding: root.padding
    property alias p_spacing: root.spacing
    property real  __appliedWidth: root.padding * 2 +
        root.spacing * (root.children.length - 0)
    //  为什么改成 `- 0` 才正常? 为什么不是 `- 1`?
    property var   __dynamicChildren: Array()
    property real  __dynamicChildrenLength: 0
    property real  __restWidth: root.width - __appliedWidth

    function _adjustDynamicChildren() {
        /*
            Usage:
                LCRow {
                    width: 20
                    p_autoWidth: true
                    Item {width: 0}  // <- this child's width will be auto calc
                    Item {width: 10}
                }
         */
        const eachWidth = __restWidth / __dynamicChildrenLength
        for (let i in __dynamicChildren) {
            __dynamicChildren[i].width = eachWidth
        }
    }
    
    function _adjustSingleDynamicChild() {
        __dynamicChildren[0].width = __restWidth
    }

    Component.onCompleted: {
        if (p_autoWidth) {
            let i, child
            for (i in root.children) {
                child = root.children[i]
                __appliedWidth += child.width
                if (child.width == 0) {
                    __dynamicChildren.push(child)
                }
            }
            
            __dynamicChildrenLength = __dynamicChildren.length
            
            if (__dynamicChildrenLength == 0) {
                p_autoWidth = false
            } else if (__dynamicChildrenLength == 1) {
                _adjustSingleDynamicChild()
                root.widthChanged.connect(_adjustSingleDynamicChild)
            } else {
                _adjustDynamicChildren()
                root.widthChanged.connect(_adjustDynamicChildren)
            }
        }

        if (p_fillHeight) {
            for (let i in root.children) {
                root.children[i].height = root.height
            }
        }

        if (p_alignCenter) {
            for (let i in root.children) {
                root.children[i].anchors.verticalCenter = root.verticalCenter
            }
        }

        console.log('[LCRow:35]', root.x, root.y, root.width, root.height)
        for (let i in root.children) {
            const x = root.children[i]
            console.log('[LCRow:38]', x.x, x.y, x.width, x.height)
        }
    }
}
