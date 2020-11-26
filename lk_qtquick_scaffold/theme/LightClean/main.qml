import QtQuick 2.15

LCWindow {

    Component.onCompleted: {
        // TODO: iterate children recursively, set child items which has
        PyHooks.scanning_qml_tree(_root)
        // TODO: enumerate methods related to PyHandler.
    }
}
