import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.14
import LightClean 1.0
import LightClean.LCButtons 1.0

Window {
    id: _root
    // color: "#F2F2F2"
    visible: true
    width: 800; height: 370

    LCFlatButton {
        id: _btn
        p_width: 100; p_height: 100
        p_text: "234234"
    }

    Component.onCompleted: {
        // console.log(_btn.background)
        // console.log(_btn.background.color)
        // console.log(_btn.contentItem.children[0])
        // console.log(_btn.contentItem.children[0].text)
    }
}
