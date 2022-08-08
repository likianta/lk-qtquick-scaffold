import QtQuick 2.15

MouseArea {
    property int  demoValue: 0
    property bool __switch: false
    onClicked: {
        this.__switch = !this.__switch
        this.demoValue = this.__switch ? 1 : 0
    }
}
