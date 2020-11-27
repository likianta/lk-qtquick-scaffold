import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import LightClean 1.0
import LightClean.LCButtons 1.0

Window {
    color: "#FFFFFF"
    visible: true
    width: 800; height: 600
    
    Column {
        anchors.centerIn: parent
        spacing: 10
        
        LCEditField {
            width: 400; height: 40
            
            p_hint: "Input your name"
            p_title: "Username"
            p_value: "Likianta D"
        }
        
        LCEditField {
            width: 400; height: 40
            
            p_digitOnly: true
            p_hint: "Input your password"
            p_title: "Password"
            p_value: ""
        }
        
        LCButton {
            anchors.horizontalCenter: parent.horizontalCenter
            width: 120; height: 40
            p_text: "START"
        }
        LCButton {
            anchors.horizontalCenter: parent.horizontalCenter
            p_text: "STOP"
        }
        LCButton {
            anchors.horizontalCenter: parent.horizontalCenter
            p_autoSize: true
            p_text: "DO IT FOREVER LONG"
        }
    }    
}
