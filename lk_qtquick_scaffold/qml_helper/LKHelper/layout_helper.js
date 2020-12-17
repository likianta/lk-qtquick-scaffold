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

function weakCenter(item, parent) {
    item.x = parent.x + parent.width / 2 - item.width / 2
    item.y = parent.y + parent.height / 2 - item.height / 2
}


function calcSpan(item1, item2) {
    // 计算从 item1 的左边到 item2 的右边的距离
    return (item2.x + item.width - item1.x)
}


function calcRelPos(source, target) {
    /*  Calculate relative position | 计算从 source 组件相对于 target 组件的 x 和 y.

        Args:
            source: (QObject)
            target: (null|QObject)
                null: 表示这是一个根布局
                QObject: 表示这是一个非根布局 (但必须是 source 的父级对象)

        Returns:
            {'x': int x, 'y': int y}

        实现思路:
            由于默认情况下, 我们只能获得 source 相对于它的直接父对象的 x 和 y. 所以我们采用
            向上递归的方式, 获取所有层级的父对象相对于其祖父对象的 x 和 y, 并加起来, 直到遇到
            祖父对象匹配到 target 为止.
            如何识别祖父对象匹配到了 target? 目前我们用的方法是判断 objectName 是否符合.
            为了保证此方法正确, 请按照下列 '注意事项' 进行.

        注意事项:
            1. target 必须有 objectName, 且 objectName 必须是有效且唯一的
            2. target 必须是 source 的父组件 (可以是任意的父级, 最高到根布局)

        其他说明事项:
            在大多数情况下, 您不需要使用本方法. 只需要使用 Item.mapToItem 即可.
            如下所示:
                Item {
                    id: target
                    Item {
                        id: source
                        Component.onCompleted: {
                            let coord1 = source.mapToItem(target, 0, 0)
                            let coord2 = LayoutHelper.calcRelPos(source, target)
                            // -> coord1.x, coord1.y 与 coord2.x, coord2.y 结果是
                            //    相同的!
                        }
                    }
                }
     */

    const targetName = (target === null) ? '__root__' : target.objectName
    if (!targetName) {
        throw 'You must define a objectName to the `target` object!'
    }
    // else {
    //     console.log('[layout_helper.js:100]',
    //                 'The target name is: ' + targetName)
    // }

    function recur(node, targetName, holdx, holdy) {
        if (node === null || node.objectName == targetName) {
            return {
                'x': holdx,
                'y': holdy,
            }
        } else {
            holdx += node.x
            holdy += node.y
            return recur(node.parent, targetName, holdx, holdy)
        }
    }

    return recur(source, targetName, 0, 0)
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
