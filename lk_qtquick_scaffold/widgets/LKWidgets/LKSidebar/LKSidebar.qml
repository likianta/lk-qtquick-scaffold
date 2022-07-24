import QtQuick 2.15
import ".."
import "../LKButtons"

LKRectangle {
    id: root
    width: pysize.sidebar_width
    height: pysize.sidebar_height
    color: pycolor.sidebar_bg

    property var  model
    //  [dict, ...]
    //      dict:
    //          required keys:
    //              text: str
    //          optional keys:
    //              icon: str
    //              color: str

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
        reuseItems: root.reuseItems
        spacing: pysize.spacing_m

        delegate: LKGhostButton {
            width: _listview.width
            height: pysize.button_height_l
            iconColor: modelData.color
            iconSize: 28
            iconSource: modelData.icon
            text: modelData.text

            property int index: model.index

            onClicked: {
                root.clicked(this.index, this.text)
                _listview.currentIndex = this.index
            }

            Component.onCompleted: {
//                this.textDelegate.horizontalAlignment = Text.AlignLeft
                this.selected = Qt.binding(() => {
                    return this.index == _listview.currentIndex
                })
            }
        }

//        delegate: LKRow {
//            id: _item
//            width: _listview.width
//            height: pysize.button_height_l
//            alignment: 'vcenter'
//            autoSize: true
//            spacing: 0
//
//            property int index: model.index
//
//            LKIcon {
//                source: modelData.icon
//                color: modelData.color
//                size: 28
//            }
//
//            LKGhostButton {
//                width: 0
//                text: modelData.text
//                onClicked: {
//                    root.clicked(_item.index, this.text)
//                    _listview.currentIndex = _item.index
//                }
//                Component.onCompleted: {
//                    this.textDelegate.horizontalAlignment = Text.AlignLeft
//                    this.selected = Qt.binding(() => {
//                        return _item.index == _listview.currentIndex
//                    })
//                }
//            }
//        }

        Component.onCompleted: {
//            this.model = root.model
            this.model = PyListView.fill_model(
                root.model,
                {'text': '', 'icon': '', 'color': ''},
                'text'
            )
        }
    }
}
