import QtQuick 2.15

Text {
    id: root
    color: pycolor.text_default
    font.family: pyfont.font_default
    font.pixelSize: pyfont.size_m
    wrapMode: Text.Wrap

    property real   maxContentWidth
    property string maxText: ''

    onMaxTextChanged: {
        const old = this.text
        this.text = maxText
        this.maxContentWidth = this.contentWidth
        this.text = old
    }
}
