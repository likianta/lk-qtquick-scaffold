import QtQuick 2.15
import QtQuick.Controls 2.15
import "../Spec/geometry.js" as Geometry
import "../Spec/palette.js" as Palette

Popup {
    id: _root
    // 在定义时, 写的都是它的末状态. 比如 `anchors.centerIn: Overlay.overlay`.
    anchors.centerIn: Overlay.overlay
    closePolicy: Popup.CloseOnEscape
    modal: true
    width: p_endW; height: p_endH

    property alias obj_Loader: _loader
    property int p_endW: 380; property int p_endH: 270
    property int __endX: _root.x; property int __endY: _root.y
    property int p_startW: 0; property int p_startH: 0
    property int p_startX: 0; property int p_startY: 0  // FIXME: no effect

    property int __duration1: 100  // product: 100; debug: 100 * 15 ~ 20
    property int __duration2: 250  // product: 250; debug: 250 * 15 ~ 20
    property int __duration3: 400  // product: 400; debug: 400 * 15 ~ 20

    property bool p_active: false
    onP_activeChanged: {
        if (p_active) {
            _root.open()
        } else {
            _root.close()
        }
    }
    onOpenedChanged: {  // to resolve insufficient closing when user pressed escape.
        if (p_active && !_root.opened) {
            p_active = _root.opened
        }
    }

    signal clicked

    background: Rectangle {
        id: _bg
        border.color: Palette.BORDER_NORMAL
        border.width: 1
        clip: true
        color: Palette.BG_WHITE
        radius: Geometry.RADIUS_POPUP

        Loader {
            id: _loader
            anchors.fill: parent
        }

        // close button
        Item {
            id: _close
            anchors.right: parent.right
            anchors.top: parent.top
            width: 40; height: 20

            MyText {
                //anchors.centerIn: parent
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                p_color: Palette.TEXT_OPT
                p_size: 12
                p_text: "Done"
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    p_active = false
                    _root.clicked()
                }
            }

            // the close button showed when popup fully opened
            //states: [
            //    State {
            //        when: p_active && _root.width > p_endW * 0.2
            //        PropertyChanges { target: _close; opacity: 1.0 }
            //    }
            //    //State {
            //    //    when: !p_active && _root.width > p_endW * 0.7
            //    //    PropertyChanges { target: _close; opacity: 0.0 }
            //    //}
            //]
            //transitions: Transition {
            //    NumberAnimation {
            //        duration: __duration3
            //        easing.type: Easing.OutQuart
            //        property: "opacity"
            //    }
            //}
        }
    }

    enter: Transition {
        NumberAnimation {
            duration: __duration1
            from: 0.0; to: 1.0
            property: "opacity"
        }
        NumberAnimation {
            duration: __duration3
            easing.type: Easing.OutQuart  // slowly goes to the end.
            from: p_startW; to: p_endW
            property: "width"
        }
        NumberAnimation {
            duration: __duration3
            easing.type: Easing.OutQuart  // slowly goes to the end.
            from: p_startH; to: p_endH
            property: "height"
        }
        //NumberAnimation {
        //    duration: __duration3
        //    easing.type: Easing.InOutQuart
        //    from: p_startX; to: __endX
        //    property: "x"  // set different effects on x and y to make the
        //    //  routine bacome a curve line.
        //}
        //NumberAnimation {
        //    duration: __duration3
        //    easing.type: Easing.OutInCubic
        //    from: p_startY; to: __endY
        //    property: "y"
        //}
    }
    exit: Transition {
        NumberAnimation {
            duration: __duration2
            from: 1.0; to: 0.0
            property: "opacity"
        }
        NumberAnimation {
            duration: __duration2
            //easing.type: Easing.InCubic
            from: p_endW; to: p_startW
            property: "width"
        }
        NumberAnimation {
            duration: __duration2
            //easing.type: Easing.InCubic
            from: p_endH; to: p_startH
            property: "height"
        }
    }

    Overlay.modal: Rectangle {
        color: "#50000000"
    }
}
