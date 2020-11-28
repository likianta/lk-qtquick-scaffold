import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCStyle/dimension.js" as LCDimension

ListView {
    id: root
    boundsBehavior: Flickable.DragOverBounds  // stop bouncing from scrolling to the start/end.
    clip: true
    maximumFlickVelocity: 2300  // control mouse wheel velocity a little faster than default
    model: p_model
    spacing: LCDimension.VSpacingXS

    property alias p_currentIndex: root.currentIndex
    property alias p_delegate: root.delegate
    property var   p_model: Array()  // [(str|dict), ...]
    property alias p_spacing: root.spacing
    property int   r_count: p_model.length
    property alias r_currentItem: root.currentItem

    // show scroll bar
    // https://stackoverflow.com/questions/45650226/qml-attach-scrollbar-to-listview/45651291
    ScrollBar.vertical: ScrollBar {}

    Component.onCompleted: {
        if (root.height == 0) {
            root.height = childrenRect.height
        }
    }
}