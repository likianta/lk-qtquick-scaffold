import QtQuick 2.15
import ".."

LKRectangle {
    id: root
    width: 0
    height: pysize.button_height
    border.width: showGhostBorder ? (_area.containsMouse ? 1 : 0) : 0
    border.color: pycolor.border_default
    color:
        _area.containsPress ? colorBgPressed :
        _area.containsMouse ? colorBgHovered :
        'transparent'

    property bool   checkable: true
    property bool   checked: false
    property string colorBgHovered: 'transparent'
    //  or pycolor.button_bg_hovered
    property string colorBgPressed: pycolor.button_bg_pressed
    property int    indicatorSize: pysize.indicator_size
    property bool   showGhostBorder: false
    property string text
    property int    __padding: pysize.padding_m

    signal clicked()
    signal toggled(bool checked)

    LKRectangle {
        id: _indicator
        anchors {
            left: parent.left
            leftMargin: root.__padding
            verticalCenter: parent.verticalCenter
        }
        width: root.indicatorSize
        height: root.indicatorSize
        border.width: 1
        border.color: pycolor.border_default
        color: 'transparent'

        Image {
            visible: root.checked
            anchors {
                fill: parent
                margins: 1
            }
            source: '.assets/check.svg'
        }
    }

    LKText {
        anchors {
            left: _indicator.right
            leftMargin: root.__padding
            verticalCenter: parent.verticalCenter
        }
        color: root.checkable ? pycolor.text_default : pycolor.text_disabled
        text: root.text
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if (root.checkable) {
                root.checked = !root.checked
                root.clicked()
            }
        }
    }

    Component.onCompleted: {
        this.checkedChanged.connect(() => this.toggled(this.checked))
        if (this.width == 0) {
            this.width = this.childrenRect.width * 1.5
        }
    }
}

