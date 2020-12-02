function easyAlign(item, alignment) {
    /*  Text.Align*
     *       Text.AlignLeft: 1
     *       Text.AlignHCenter: 4
     *       Text.AlignRight: 2
     *       Text.AlignTop: 32
     *       Text.AlignBottom: 64
     *       Text.AlignVCenter: 128
     *  PS: TextInput.Align* are same with above.
     *  See:
     *      LCEdit
     *      LCText
     */
    switch (alignment) {
        case 'center':
            item.horizontalAlignment = 4
            item.verticalAlignment = 128
            break
        case 'hcenter':
            item.horizontalAlignment = 4
            break
        case 'htop':
            item.horizontalAlignment = 4
            item.verticalAlignment = 32
            break
        case 'hbottom':
            item.horizontalAlignment = 4
            item.verticalAlignment = 64
            break
        case 'vcenter':
            item.verticalAlignment = 128
            break
        case 'vleft':
        // fall down
        case 'lcenter':
            item.horizontalAlignment = 1
            item.verticalAlignment = 128
            break
        case 'vright':
        // fall down
        case 'rcenter':
            item.horizontalAlignment = 2
            item.verticalAlignment = 128
            break
    }
}


function calcSpan(item1, item2) {
    // 计算从 item1 的左边到 item2 的右边的距离
    return (item2.x + item.width - item1.x)
}


function wrapWidth(root, itemType) {  // TODO
    switch (itemType) {
        case 'Button':
            root.width = root.leftInset + root.rightInset +
                root.implicitContentWidth + implicitIndicatorWidth

    }
}


function autoWidth(parent) {  // DEL
    // 宽度为 0 的组件, 采用自适应宽度; 宽度为 0 < w < 1 的组件, 采用百分比计算;
    // 宽度为 w > 1 的组件, 采用像素.
    let i, child
    let remainingWidth = parent.width -
        parent.p_spacing * (parent.children.length - 1)
    let remainingChildren = Array()

    for (i in parent.children) {
        child = parent.children[i]
        if (child.width == 0) {
            remainingChildren.push(child)
        } else if (child.width < 1) {
            child.width *= parent.width
        } else {
            // pass
        }
        remainingWidth -= child.width
    }

    if (remainingWidth > 0) {
        const eachRemainingChildWidth = remainingWidth / remainingChildren.length
        for (i in remainingChildren) {
            child = remainingChildren[i]
            child.width = eachRemainingChildWidth
        }
    }
}


function autoHeight(parent) {  // DEL
    // See also `autoWidth`
    let i, child
    let remainingHeight = parent.height -
        (parent.topPadding + parent.bottomPadding) -
        (parent.p_spacing * (parent.children.length - 1))
    let remainingChildren = Array()

    for (i in parent.children) {
        child = parent.children[i]
        if (child.height == 0) {
            remainingChildren.push(child)
        } else if (child.height < 1) {
            child.height *= parent.height
        } else {
            // pass
        }
        remainingHeight -= child.height
    }

    if (remainingHeight > 0) {
        const eachRemainingChildHeight = remainingHeight / remainingChildren.length
        for (i in remainingChildren) {
            child = remainingChildren[i]
            child.height = eachRemainingChildHeight
        }
    }
}
