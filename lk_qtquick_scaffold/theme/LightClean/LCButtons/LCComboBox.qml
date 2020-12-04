import QtQuick 2.15
import QtQuick.Controls 2.15
import LKHelper
import "../"
import "../LCBackground"
import "../LCStyle/dimension.js" as LCDimension

ComboBox {
    id: root
    // implicitWidth: root.contentWidth
    // implicitHeight: LCDimension.ButtonHeightS
    editable: false
    hoverEnabled: true

    property alias p_active: root.down  // true means the popup visible (expand)
    property alias p_editable: root.editable
    property alias p_model: root.model

    background: LCRectBg {
        p_borderless: p_active  // no border when active; else show border in
        //  normal state
    }

    delegate: LCGhostBg {
        p_hovered: root.hovered

        Loader {
            id: _iconLoader
            anchors.left: parent.left
            anchors.leftMargin: LCDimension.MarginM
            anchors.verticalCenter: parent.verticalCenter
            implicitWidth: LCDimension.IconWidth
            implicitHeight: LCDimension.IconHeight
            sourceComponent: Image {
                id: _icon
                // ...
            }
        }

        LCText {
            anchors.left: _iconLoader.right
            anchors.leftMargin: LCDimension.MarginM
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            p_alignment: 'lcenter'
        }
    }

    indicator: Image {
        id: _indicator
        implicitWidth: LCDimension.IconWidth
        implicitHeight: LCDimension.IconHeight
        fillMode: Image.Pad
        source: '../rss/caret-left.svg'

        states: [
            State {
                when: root.p_active
                PropertyChanges {
                    target: _indicator
                    rotation
                }
            }
        ]

        Component.onCompleted: {
            LayoutHelper.easyAlign(this, 'center')
        }
    }
}
