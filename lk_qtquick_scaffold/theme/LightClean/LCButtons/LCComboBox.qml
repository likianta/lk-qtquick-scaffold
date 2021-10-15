import QtQuick
import QtQuick.Controls
import "../" as LC

ComboBox {
    id: root
//    width: (4 + root._txt_width + 12) + icon.width
    height: 24
//    z: 1

    property alias  p_model: root.model
    property int    p_radius: 4
    property int    p_size: 11 // item font size

    property int    _anim_duration: 300 // unit: ms
    property bool   _opened: false
    property int    _pop_width: 0
    property int    _pop_height: 0
    property int    _txt_width: txt._content_width

    onModelChanged: {
        //  measure popup list width and height
        var res = LKLayoutHelper.calc_model_size(root.p_model, 10, 24)
        root._pop_width = res[0]
        root._pop_height = res[1]
        console.log(res, root._pop_width, root._pop_height)
    }

    component ItemText: LC.LCText {
        leftPadding: 4
        p_alignment: 'lcenter'
        p_bold: true
        p_size: root.p_size
//        p_text: p_value
//        required property string p_value
    }

    background: LC.LCRectangle {
        id: bg
        border.width: 1
        border.color: '#0984d8'
        color: '#ffffff'
        height: root._opened ? root._pop_height : root.height
        radius: root.p_radius

        Behavior on height {
            NumberAnimation {
                duration: root._anim_duration
                easing.type: Easing.OutQuart
            }
        }
    }

    contentItem: ItemText {
        id: txt
        p_text: root.displayText
        property alias _content_width: txt.contentWidth

//        Behavior on p_color {
//            ColorAnimation {
//                duration: 100
//                property: 'p_color'
//            }
//        }

//        Component.onCompleted: {
//            console.log(this._content_width)
//        }
    }

    indicator: Image {
        id: icon
        x: root.width - 24
        y: (root.height - icon.height) / 2
        width: 24
        height: 24
        rotation: root._opened ? -90 : 0
        source: RMAssets.get('arrow-drop-left-line.svg')

        Behavior on rotation {
            NumberAnimation {
                duration: root._anim_duration
                easing.type: Easing.OutQuart
            }
        }
    }

    popup: Popup {
        id: pop
        y: root.height
        width: root.width
        height: root._pop_height
        clip: true

        background: Item {}
        contentItem: ListView {
            height: contentHeight
//            height: pop.visible ? contentHeight : 0

//            clip: true
            currentIndex: root.highlightedIndex
            model: root.model
            opacity: root._opened ? 1 : 0
            reuseItems: true
            spacing: 4

            delegate: LC.LCRectangle {
                width: root._pop_width + 12
                height: _txt.height + 2
                p_color: _area.containsMouse ? '#EEEEEE' : '#FFFFFF'

                ItemText {
                    id: _txt
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                    p_text: modelData
                }

                Image {
                    anchors.right: parent.right
                    anchors.rightMargin: 4
                    anchors.verticalCenter: parent.verticalCenter
//                    x: parent.width + 2
//                    y: parent.height / 2 - 4
                    width: 4
                    height: 4
//                    source: RMAssets.get('record-circle-fill.svg')
                    source: RMAssets.get('checkbox-blank-circle-fill.svg')
                    visible: index == root.highlightedIndex
                }

                MouseArea {
                    id: _area
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        root.currentIndex = index
                        pop.close()
                    }
                }
            }

            Behavior on opacity {
                NumberAnimation {
                    duration: root._anim_duration
//                    easing.type: Easing.OutQuart
                }
            }
        }

        onClosed: {
            root._opened = false
        }

        onOpened: {
            root._opened = true
        }
    }

    Component {
        id: txtComp

        LC.LCText {
            id: txt
            leftPadding: 4
            p_alignment: 'lcenter'
            p_bold: true
            p_size: root.p_size
        }
    }

    Component.onCompleted: {
        root.width = Qt.binding(() => root._pop_width + icon.width)
    }
}