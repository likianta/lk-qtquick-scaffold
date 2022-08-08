// https://stackoverflow.com/questions/1337523/measuring-text-width-in-qt
import QtQuick 2.15

LKText {
    id: root

    property string maxText
    property int    maxWidth

    onMaxTextChanged: {
        this.maxWidth = measureContent(this.maxText)
    }

    function measureContent(text) {
        return _metrics.advanceWidth(text)
    }

    FontMetrics {
        id: _metrics
        font: root.font
    }
}
