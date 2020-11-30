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


function autoWidth(parent) {
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

    const eachRemainingChildWidth = remainingWidth / (remainingChildren.length)
    for (i in remainingChildren) {
        child = remainingChildren[i]
        child.width = eachRemainingChildWidth
    }
}


function autoHeight(parent) {
    let i, child
    let remainingHeight = parent.height -
        parent.p_spacing * (parent.children.length - 1)
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

    const eachRemainingChildHeight = remainingHeight / (remainingChildren.length)
    for (i in remainingChildren) {
        child = remainingChildren[i]
        child.height = eachRemainingChildHeight
    }
}
