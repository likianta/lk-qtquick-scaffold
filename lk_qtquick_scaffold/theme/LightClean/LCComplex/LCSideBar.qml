import QtQuick
import QtQuick.Controls
import ".." as LC

Control {
    id: root

    property alias  p_background: root.background
    property alias  p_model: listview.model

    component mItem: LC.LCRectangle {
        id: _item
        p_color: _area.p_hovered ? '' : 'transparent'

        property _padding: 4

        property string p_desc: ''
        property string p_icon: ''
        property string p_title

        Image {
            id: _img
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.margins: parent._padding
            width: _item.p_icon ? 36 : 0
            height: _img.width
            source: _item.p_icon
        }

        LC.LCText {
            id: _title
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: parent._padding
            p_alignment: 'lcenter'
            p_text: _item.p_title
        }

        LC.LCText {
            anchors.left: parent.left
            anchors.top: _title.bottom
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: parent._padding
            wrapMode: Text.Wrap
            p_alignment: 'ltop'
            p_color: '#EEEEEE'
            p_text: _item.p_desc
        }

        LC.LCMouseArea {
            id: _area
        }
    }

    ListView {
        id: listview
        anchors.fill: parent
        reuseItems: true

        delegate: mItem {
            width: listview.width
            implicitHeight: 120
            /*  The model example
             *
             *  ListModel {
             *      ListElement {
             *          m_desc: ''
             *          m_icon: ''
             *          m_title: ''
             *      }
             *      ...
             *  }
             */
            p_desc: m_desc
            p_icon: m_icon
            p_title: m_title
        }
    }
}
