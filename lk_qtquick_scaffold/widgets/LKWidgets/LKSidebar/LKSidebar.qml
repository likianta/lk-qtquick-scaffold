import QtQuick 2.15
import ".."
import "../LKButtons"

LKRectangle {
    id: root
    width: pysize.sidebar_width
    height: pysize.sidebar_height
    color: pycolor.sidebar_bg

    property var  model
    property bool reuseItems: true

    signal clicked(int index, string text)

    ListView {
        id: _listview
        anchors {
            fill: parent
            leftMargin: pysize.margin_m
            rightMargin: pysize.margin_m
            topMargin: pysize.margin_s
            bottomMargin: pysize.margin_s
        }
        model: root.model
        reuseItems: root.reuseItems
        spacing: pysize.spacing_m

        delegate: LKGhostButton {
            width: _listview.width
            height: pysize.button_height_l
            text: modelData
            property int index: model.index
            onClicked: {
                root.clicked(this.index, this.text)
                _listview.currentIndex = this.index
            }
            Component.onCompleted: {
                this.textDelegate.horizontalAlignment = Text.AlignLeft
                this.selected = Qt.binding(() => {
                    return this.index == _listview.currentIndex
                })
            }
        }
    }
}
