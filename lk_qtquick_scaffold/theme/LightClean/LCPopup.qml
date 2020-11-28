import QtQuick 2.15
import QtQuick.Controls 2.15
import "./LCStyle/dimension.js" as LCGeometry
import "./LCStyle/motion.js" as LCMotion
import "./LCStyle/palette.js" as LCPalette

Popup {
    id: root
    // 在定义时, 写的都是它的末状态. 比如 `anchors.centerIn: Overlay.overlay`.
    anchors.centerIn: Overlay.overlay
    closePolicy: Popup.CloseOnEscape
    modal: true  // Forbit user's click event outside the popup window.
    width: p_endW; height: p_endH

    property bool p_active: false
    property int  p_startW: 0;    property int p_startH: 0
    property int  p_endW: 380;    property int p_endH: 270
    property int  p_startX: 0;    property int p_startY: 0  // FIXME: no effect
    property int  __endX: root.x; property int __endY: root.y

    onP_activeChanged: {
        if (p_active) {
            root.open()
        } else {
            root.close()
        }
    }
    onOpenedChanged: {
        // to resolve insufficient closing when user pressed escape.
        if (p_active && !root.opened) {
            p_active = root.opened
        }
    }

    background: Rectangle {
        id: _bg
        border.color: LCPalette.BorderNormal
        border.width: 1
        clip: true
        color: LCPalette.BgWhite
        radius: LCGeometry.RadiusM
    }

    contentItem: Item {
        Item {  // close button
            id: _close
            anchors.right: parent.right
            anchors.top: parent.top
            width: LCGeometry.ButtonCloseWidth; height: LCGeometry.ButtonCloseHeight
            z: 1

            LCText {
                anchors.centerIn: parent
                p_color: LCPalette.ThemeLightBlue
                p_size: 12
                p_text: "Done"
            }

            MouseArea {
                anchors.fill: parent
                onClicked: root.close()
            }
        }
    }

    enter: Transition {
        // 进场动画: 从窗口中心点开始, 宽和高从 0 增加到最终尺寸, 由透明变为不透
        // 明, 动画速度由快到慢, 以强化完成时的动画印象. 透明度动画要比尺寸变化
        // 快一些, 以避免动画拖沓.
        NumberAnimation {
            property: "opacity"
            duration: LCMotion.Soon
            from: 0.0; to: 1.0
        }
        NumberAnimation {
            property: "width"
            duration: LCMotion.Soft
            easing.type: Easing.OutQuart  // slowly goes to the end.
            from: p_startW; to: p_endW
        }
        NumberAnimation {
            property: "height"
            duration: LCMotion.Soft
            easing.type: Easing.OutQuart  // slowly goes to the end.
            from: p_startH; to: p_endH
        }
        // NumberAnimation {
        //     property: "x"  // set different effects on x and y to make the
        //     //  routine bacome a curve line.
        //     duration: LCMotion.Soft
        //     easing.type: Easing.InOutQuart
        //     from: p_startX; to: __endX
        // }
        // NumberAnimation {
        //     property: "y"
        //     duration: LCMotion.Soft
        //     easing.type: Easing.OutInCubic
        //     from: p_startY; to: __endY
        // }
    }

    exit: Transition {
        NumberAnimation {
            property: "opacity"
            duration: LCMotion.Swift
            from: 1.0; to: 0.0
        }
        NumberAnimation {
            property: "width"
            duration: LCMotion.Swift
            from: p_endW; to: p_startW
        }
        NumberAnimation {
            property: "height"
            duration: LCMotion.Swift
            from: p_endH; to: p_startH
        }
    }

    Overlay.modal: Rectangle {
        color: "#50000000"
    }
}
