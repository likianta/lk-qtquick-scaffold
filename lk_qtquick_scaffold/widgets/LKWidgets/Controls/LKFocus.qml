import QtQuick 2.15

Item {
    id: root

    property bool   active: false
    property string scope: 'global'
    property string __sid: generateRandomId()
    property var    __registeredFuncs: Object()

    signal triggered(string fid)

    onActiveChanged: {
        if (root.active) {
            lkscope.activate_scope(root.scope, root.__sid)
        } else {
            lkscope.deactivate_scope(root.scope, root.__sid)
        }
    }

    function generateRandomId() {
        return pyside.eval(`
            from uuid import uuid1
            return uuid1().hex
        `)
    }

    function register(key, modifier, func) {
        const sid = root.__sid
        const fid = root.generateRandomId()
        lkscope.register_func(
            root.scope, sid, fid, root, key, modifier
        )
        root.__registeredFuncs[fid] = func
    }

    Component.onCompleted: {
        lkscope.register_scope(root.scope, root.field)
        root.triggered.connect((fid) => {
            root.__registeredFuncs[fid]()
        })
        root.activeChanged()
    }
}
