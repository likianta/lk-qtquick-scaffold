import QtQuick
import QtQuick.Controls
import "../"

ComboBox {
    id: root
    width: (4 + root._txt_width + 12) + icon.width
    height: 24
//    z: 1

    property alias  p_model: root.model
    property int    p_radius: 4
    property int    p_size: 11 // item font size

    property int    _pop_width: 0
    property int    _pop_height: 0
    property bool   _opened: false
    property int    _txt_width: txt._content_width

    onModelChanged: {
        //  measure popup list width and height
        var res = LKLayoutHelper.calc_model_size(root.p_model)
        root._pop_width = res[0]
        root._pop_height = res[1]
        console.log(res, root._pop_width, root._pop_height)
    }

    background: LCRectangle {
        id: bg
        border.width: 1
        border.color: '#0984d8'
        color: '#ffffff'
        radius: root.p_radius

        states: [
            State {
                when: root._opened
                PropertyChanges {
                    target: bg
                    height: root._pop_height
                }
            }
        ]

        transitions: [
            Transition {
                NumberAnimation {
                    duration: 400
                    easing.type: Easing.OutQuart
                    property: 'height'
                }
            }
        ]
    }

    contentItem: LCText {
        id: txt
        leftPadding: 4
        p_alignment: 'lcenter'
        p_bold: true
        p_size: root.p_size
        p_text: root.displayText

        property alias _content_width: txt.contentWidth

        states: [
            State {
                when: root._opened
                PropertyChanges {
                    target: txt
                    p_color: '#A5A5A5'
                }
            }
        ]

        transitions: [
            Transition {
                ColorAnimation {
                    duration: 100
                    property: 'p_color'
                }
            }
        ]

        Component.onCompleted: {
            console.log(this._content_width)
        }
    }

    indicator: Image {
        id: icon
        x: root.width - 24
        y: (root.height - icon.height) / 2
        width: 24
        height: 24
        source: RMAssets.get('arrow-drop-left-line.svg')

        states: [
            State {
                when: root._opened
                PropertyChanges {
                    target: icon
                    rotation: -90
                }
            }
        ]

        transitions: [
            Transition {
                NumberAnimation {
                    duration: 400
                    easing.type: Easing.OutQuart
                    property: 'rotation'
                }
            }
        ]
    }

    popup: Popup {
        id: pop
        y: root.height
        width: root.width
        implicitHeight: root._pop_height

        background: Item {}

        onClosed: {
            root._opened = false
        }

        onOpened: {
            root._opened = true
        }
    }
}