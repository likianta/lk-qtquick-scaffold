// DELETE ME: This file is going to be removed.

function checkSize(rootItem) {
    let child

    console.log(
        'root', '\t',
        'width: ' + rootItem.width, '\t',
        'height: ' + rootItem.height, '\t',
        'x: ' + rootItem.x, '\t',
        'y: ' + rootItem.y, '\t',
    )

    for (let i in rootItem.children) {
        child = rootItem.children[i]
        console.log(
            i, '\t',
            'width: ' + child.width, '\t',
            'height: ' + child.height, '\t',
            'x: ' + rootItem.x, '\t',
            'y: ' + rootItem.y, '\t',
        )
    }
}

function checkSizeTree(rootItem, indent) {
    // this is a recursive loop
    // init call (from qml): checkSizeTree(_root, 0)

    if (indent == 0) {
        // root introduction
        console.log('|' + '-'.repeat(120))
        _sizeTreeTemplate(rootItem, 0)
    }
    indent += 1

    let child
    for (let i in rootItem.children) {
        child = rootItem.children[i]
        _sizeTreeTemplate(child, indent)
        checkSizeTree(child, indent + 1)
    }
}

function _sizeTreeTemplate(item, indent) {
    /*  :param QObject item:
     *  :param int indent: |0|4|8|12|16|...|
     */

    let prefix = '|-'
    if (indent > 0) {
        prefix = '|  '.repeat(indent) + prefix
    }
    
    console.log(
        prefix,
        item, '\t', '\t',
        'width: ' + item.width, '\t',
        'height: ' + item.height, '\t',
        'x: ' + item.x, '\t',
        'y: ' + item.y, '\t',
    )
}
