import QtQuick 2.15
import ".."

LKRectangle3 {
    id: root
    width: 0
    height: 0
    radius: pysize.button_radius
    border.width: hovered ? 1 : 0
    border.color: borderColor
    color: selected ? bgActive : (hovered ? bgHover : 'transparent')

    property string bgHover: pycolor.button_bg_hover
    property string bgActive: pycolor.button_bg_active
    property string borderColor: pycolor.border_glow
    property bool   selected: false

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = Qt.binding(() => {
                return this.textDelegate.contentWidth + pysize.padding_h_l * 2
            })
        }
        if (this.height == 0) {
            this.height = Qt.binding(() => {
                return this.textDelegate.contentHeight + pysize.padding_v_m * 2
            })
        }

        this.textDelegate.anchors.fill = Qt.binding(() => this)
        this.textDelegate.anchors.leftMargin = pysize.padding_h_l
//        this.textDelegate.anchors.verticalCenter = Qt.binding(
//            () => this.verticalCenter)
        this.textDelegate.horizontalAlignment = Text.AlignHCenter
        this.textDelegate.verticalAlignment = Text.AlignVCenter
    }
}
