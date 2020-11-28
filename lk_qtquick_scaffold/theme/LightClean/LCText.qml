import QtQuick 2.15
import "./LCStyle/palette.js" as LCPalette
import "./LCStyle/typography.js" as LCTypo

Text {
    id: root
    color: LCPalette.TextNormal
    font.pixelSize: LCTypo.FontSizeM

    property string p_alignment: "center"  // see `Component.onCompleted`
    property alias  p_bold: root.font.bold
    property alias  p_color: root.color
    property alias  p_size: root.font.pixelSize
    property alias  p_text: root.text

    Component.onCompleted: {
        switch (p_alignment) {
            case 'center':
                this.horizontalAlignment = Text.AlignHCenter
                this.verticalAlignment = Text.AlignVCenter
                break
            case 'hcenter':
                this.horizontalAlignment = Text.AlignHCenter
                break
            case 'htop':
                this.horizontalAlignment = Text.AlignHCenter
                this.verticalAlignment = Text.AlignTop
                break
            case 'hbottom':
                this.horizontalAlignment = Text.AlignHCenter
                this.verticalAlignment = Text.AlignBottom
                break
            case 'vcenter':
                this.verticalAlignment = Text.AlignVCenter
                break
            case 'vleft':
                // fall down
            case 'lcenter':
                this.horizontalAlignment = Text.AlignLeft
                this.verticalAlignment = Text.AlignVCenter
                break
            case 'vright':
                // fall down
            case 'rcenter':
                this.horizontalAlignment = Text.AlignRight
                this.verticalAlignment = Text.AlignVCenter
                break
        }
    }
}
