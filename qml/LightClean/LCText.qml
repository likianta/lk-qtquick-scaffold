import QtQuick 2.15
import "../Spec/palette.js" as Palette

Text {
    id: _root
    color: Palette.TEXT_NORMAL
    font.family: "Microsoft YaHei UI"
    font.pixelSize: 14
    horizontalAlignment: Text.AlighHCenter; verticalAlignment: Text.AlignVCenter

    property alias p_bold: _root.font.bold
    property alias p_color: _root.color
    property alias p_size: _root.font.pixelSize
    property alias p_text: _root.text  // 声明 p_text 以强调这是一个可被外部修改的属性.
}
