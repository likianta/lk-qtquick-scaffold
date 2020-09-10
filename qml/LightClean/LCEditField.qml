// edit field with an indicator
import QtQuick 2.15
import "../Spec/palette.js" as Palette

Rectangle {
    id: _root
    //width: childrenRect.width; height: 40
    height: 40

    property alias obj_Loader: _loader
    property alias p_barWidth: _loader.width
    property alias p_title: _title.p_text
    //property alias p_titleWidth: _title.width
    property bool p_digitOnly: false
    property string p_value: ""

    signal clicked

    // title
    MyText {
        id: _title
        anchors.right: _loader.left
        anchors.rightMargin: 10
        height: parent.height
        horizontalAlignment: Text.AlignRight; verticalAlignment: Text.AlignVCenter
        //width: parent.width - _loader.width; height: parent.height
    }

    // edit bar
    Loader {
        id: _loader
        anchors.right: parent.right
        width: 380; height: parent.height

        sourceComponent: MyEditbar {
            p_text: p_value
            validator: RegularExpressionValidator {
                regularExpression: p_digitOnly ? /[0-9]+/ : /.*/
            }

            onP_textChanged: _root.p_value = item.p_text
        }
    }
}
