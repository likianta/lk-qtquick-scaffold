import QtQuick 2.15
import ".."

LKRectangle3 {
    id: root
    width: 0
    height: 0
    radius: pysize.button_radius
    border.width: hovered ? 1 : 0
    border.color: borderColor
    color: selected ? bgActive : (hovered ? bgHovered : 'transparent')

    property string bgHovered: pycolor.button_bg_hovered
    property string bgActive: pycolor.button_bg_active
    property string borderColor: pycolor.border_glow
    property string iconColor
    property int    iconSize: pysize.icon_size
    property url    iconSource
    property bool   selected: false

    Loader {
        id: _icon_loader
        enabled: Boolean(root.iconSource)
        anchors {
            left: parent.left
            leftMargin: pysize.padding_h_m
            verticalCenter: parent.verticalCenter
        }
        width: root.iconSize
        height: root.iconSize
        sourceComponent: LKIcon { }
        onLoaded: {
            this.item.color = root.iconColor
            this.item.size = root.iconSize
            this.item.source = root.iconSource
        }
    }

    Component.onCompleted: {
        const text_ = this.textDelegate

        if (this.width == 0) {
            this.width = Qt.binding(() => {
                return text_.contentWidth + pysize.padding_h_l * 2
            })
        }
        if (this.height == 0) {
            this.height = Qt.binding(() => {
                return text_.contentHeight + pysize.padding_v_m * 2
            })
        }

        text_.anchors.fill = Qt.binding(() => this)
        text_.horizontalAlignment = Text.AlignHCenter
        text_.verticalAlignment = Text.AlignVCenter

        if (this.iconSource) {
            text_.leftPadding = _icon_loader.x
                + _icon_loader.width
                + pysize.padding_h_m
            text_.horizontalAlignment = Text.AlignLeft
        }
    }
}
