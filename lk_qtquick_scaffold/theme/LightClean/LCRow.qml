import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension

Row {
    id: root
    spacing: LCDimension.HSpacingM

    property bool  p_alignCenter: true
    property bool  p_enableFillRest: false
    property bool  p_fillHeight: false
    property alias p_padding: root.padding
    property alias p_spacing: root.spacing
    property real  r_fillRest: 0  // related to `p_enableFillRest`
    property real  __appliedWidth: {  // related to `p_enableFillRest`
        return (root.leftPadding + root.rightPadding) +
            (root.spacing * (root.children.length - 0))
            //  为什么改成 `- 0` 才正常? 为什么不是 `- 1`?
    }

    /*  How to use 'auto width' system?
        
        Example:
            LCRow {
                width: 100
                p_spacing: 10
                p_enableFillRest: true
                Item { width: 10 }
                Item { width: r_fillRest }  // -> 60
                Item { width: 10 }
            }
        
        Note:
            If the need-to-filled item is the last child, just use `root.width -
            secondLast.x - root.spacing` would be faster than 'auto width'.
            
        Reference:
            https://stackoverflow.com/questions/27319985/how-to-make-last-item
            -in-qml-container-fill-remaining-space
     */

    // -------------------------------------------------------------------------

    function _updateFillHeight() {
        for (let i in root.children) {
            root.children[i].height = root.height -
                root.topPadding -
                root.bottomPadding
        }
    }

    function _updateFillRest() {
        root.r_fillRest = root.width - __appliedWidth
    }

    function _initAppliedWidth() {
        for (let i in root.children) {
            __appliedWidth += root.children[i].width
        }
        if (__appliedWidth < root.width) {
            return true
        } else {
            return false
        }
    }

    Component.onCompleted: {
        if (p_alignCenter) {
            for (let i in root.children) {
                root.children[i].anchors.verticalCenter = root.verticalCenter
            }
        }

        if (p_enableFillRest) {
            if (_initAppliedWidth()) {
                _updateFillRest()
                root.widthChanged.connect(_updateFillRest)
            }
        }

        if (p_fillHeight) {
            _updateFillHeight()
            this.heightChanged.connect(_updateFillHeight)
        }

        // console.log('[LCRow:85]', root.x, root.y, root.width, root.height)
        // for (let i in root.children) {
        //     const x = root.children[i]
        //     console.log('[LCRow:88]', x.x, x.y, x.width, x.height)
        // }
    }
}
