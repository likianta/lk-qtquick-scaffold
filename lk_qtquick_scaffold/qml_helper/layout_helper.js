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
