import QtQuick 2.15

Item {
    property int  padding: 0
    property int  spacing: pysize.spacing_m
    property bool vfill: false
    Component.onCompleted: {
        pylayout.halign_children(this)
    }
}
