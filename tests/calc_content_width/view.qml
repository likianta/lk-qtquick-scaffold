import QtQuick
import LKWidgets

LKWindow {

    LKText {
        id: _t0
        text: 'hello world'
    }

    LKText {
        id: _t1
        text: 'hello world'
    }

    LKText2 {
        id: _t2
        maxText: 'hello world'
        text: 'hello world'
    }

    Component.onCompleted: {
        console.log(
            [_t0.font.family, _t0.font.pixelSize],
            [_t0.width, _t0.contentWidth],
            [pylayout.calc_content_width(_t1.text),
             pylayout.calc_content_width(_t1.text, _t1)],
            [_t2.maxWidth],
        )
    }
}
