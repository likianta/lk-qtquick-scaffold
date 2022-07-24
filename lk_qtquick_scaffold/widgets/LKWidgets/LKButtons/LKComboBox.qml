import QtQuick 2.15
import QtQuick.Controls 2.15
import ".."

Item {
    id: root
    width: 0
    height: pysize.button_height
    clip: false

    property string colorBgDefault: pycolor.panel_bg
    property string colorBgHovered: pycolor.button_bg_hovered
    //  or pycolor.button_bg_hovered
    property string colorBgPressed: pycolor.button_bg_pressed
    property int    currentIndex: 0
    property int    dropdownHeight: 0
    property string dropdownBgColor: colorBgDefault
    property string dropdownBorderColor: _display.border.color
    property bool   expandable: true
    property alias  expanded: _dropdown.opened
    //  this is readonly. it is controled by _dropdown's opened and closed
    //  signal.
    property bool   editable: false  // TODO
    property int    indicatorSize: pysize.indicator_size
    property var    model  // list[str]
    property bool   wheelEnabled: true  // TODO
    property int    __padding: pysize.padding_m

    signal clicked(int index, string text)

    component MyItem: LKRectangle {
        width: root.width
        height: pysize.button_height
        border.width: 0
        border.color: pycolor.border_default
        color: {
            if (root.expandable) {
                if (_area.containsPress) {
                    return root.colorBgPressed
                } else if (_area.containsMouse) {
                    return root.colorBgHovered
                } else {
                    return root.colorBgDefault
                }
            } else {
                return root.colorBgDefault
            }
        }

        property alias hovered: _area.containsMouse
        property alias pressed: _area.containsPress
        property alias textDelegate: _text

        signal clicked()

        LKText {
            id: _text
            anchors {
                left: parent.left
                leftMargin: root.__padding
                verticalCenter: parent.verticalCenter
            }
            color: root.expandable ?
                pycolor.text_default : pycolor.text_disabled
        }

        MouseArea {
            id: _area
            anchors.fill: parent
            hoverEnabled: true
            onClicked: parent.clicked()
        }
    }

    MyItem {
        id: _display
        border.width: 1
        textDelegate.text: root.model[root.currentIndex]

        onClicked: {
            if (root.expandable) {
                if (root.expanded) {
                    _dropdown.close()
                } else {
                    _dropdown.open()
                }
            }
        }

        Image {
            id: _indicator
            anchors {
                right: parent.right
                rightMargin: root.__padding
                verticalCenter: parent.verticalCenter
            }
            width: root.indicatorSize
            height: root.indicatorSize
            rotation: root.expanded ? 0 : 90
            source: '.assets/chevron-down-arrow.svg'
    //        sourceSize.width: root.indicatorSize - 2  // -2 for better appearance
    //        sourceSize.height: root.indicatorSize
            Behavior on rotation {
                NumberAnimation {
                    duration: 100
                }
            }
        }
    }

    Popup {
        id: _dropdown
        y: _display.height + root.__padding
        width: root.width
        height: root.dropdownHeight
        clip: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        background: LKRectangle {
            width: parent.width
            height: root.expanded ? parent.height : 0

            border.width: 1
            border.color: root.dropdownBorderColor
            color: root.dropdownBgColor

            Behavior on height {
                NumberAnimation {
                    duration: 100
                }
            }
        }

        contentItem: LKListView {
            anchors.fill: parent
            anchors.margins: pysize.margin_s
            model: root.model
            spacing: pysize.spacing_s

            delegate: MyItem {
                textDelegate.text: modelData
                property int index: model.index
                onClicked: {
                    root.currentIndex = this.index
                    root.clicked(this.index, this.textDelegate.text)
                    _dropdown.close()
                }
            }
        }

        Component.onCompleted: {
            if (this.height == 0) {
                const totalHeight = (
                    pysize.margin_s * 2 +
                    pysize.button_height
                ) * root.model.length + (
                    pysize.spacing_m * (root.model.length - 1)
                )
                if (totalHeight > pysize.listview_height) {
                    this.height = pysize.listview_height
                } else {
                    this.height = totalHeight
                }
            }
        }
    }

    Component.onCompleted: {
        if (this.width == 0) {
            // get longest item of model
            const longestContent = pyside.eval(`
                return max(map(str, model), key=len)
            `, {'model': root.model})
//            console.log(longestContent)

            _display.textDelegate.text = longestContent
            this.width = (
                _display.textDelegate.contentWidth +
                root.indicatorSize +
                root.__padding * 3
            ) * 1.5

            // restore text binding
            _display.textDelegate.text = root.model[root.currentIndex]
            _display.textDelegate.text = Qt.binding(() => {
                return root.model[root.currentIndex]
            })
        }
    }
}
