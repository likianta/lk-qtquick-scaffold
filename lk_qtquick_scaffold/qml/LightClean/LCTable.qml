import QtQuick 2.14
import QtQuick.Controls 2.14
import "./LCStyle/geometry.js" as LCGeometry

ScrollView {
    id: _root
    anchors.margins: LCGeometry.MarginM
    // clip: true
    contentWidth: __realContentWidth; contentHeight: childrenRect.height

    property var p_header
    //      [str title, ...]
    property alias p_model: _rows.model
    //      [{title: value}, ...]. assert p_model[0].keys() == p_header
    property var __childrenWidthsManager: Array(p_header.length)
    //      [headerCell1, headerCell2, ...]. assert len(self) == len(p_header)
    //      this variant will be initialized when `p_header` completed.
    property int __realContentWidth: 0
    property int __scrollSpeed: 30

    function fn__updateContentWidth(m, n) {
        __realContentWidth = __realContentWidth - m + n
        // console.log("LCTable.qml:24", __realContentWidth)
    }

    // -------------------------------------------------------------------------
    // the main table

    Item {
        id: _mainTable
        height: parent.height

        ListView {
            id: _rows
            anchors.left: parent.left
            anchors.top: _header.bottom
            height: parent.height
            orientation: ListView.Vertical
            spacing: 0

            delegate: Row {
                id: _row
                height: LCGeometry.BarHeight
                spacing: 0

                property int __rowx: model.index

                Repeater {
                    id: _cells
                    model: p_header
                    delegate: LCRectangle {
                        id: _cell
                        //clip: true
                        height: parent.height

                        p_border.width: 1
                        p_radius: 0

                        property bool p_clickable: false
                        property string p_title
                        signal fn_clicked

                        LCText {
                            id: _txt
                            anchors.centerIn: parent
                            p_text: _rows.model[__rowx][p_title]
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                if (p_clickable) {
                                    parent.fn_clicked()
                                }
                            }
                        }

                        Component.onCompleted: {
                            p_title = modelData
                            // console.log("LCTable.qml:81#_cell", '_cell initializing')

                            // adjust cell width
                            const preferredWidth = _txt.width + LCGeometry.HSpacingM * 2
                            const m = __childrenWidthsManager[model.index].width
                            const n = preferredWidth
                            if (m < n) {
                                __childrenWidthsManager[model.index].width = preferredWidth
                                fn__updateContentWidth(m, n)
                            }
                            // hook up width in strong reference
                            _cell.width = __childrenWidthsManager[model.index].width
                            console.log("LCTable.qml:97#_cell", model.index, _cell.width)
                        }
                    }
                }
            }
        }

        // -------------------------------------------------------------------------
        // the header

        Row {
            id: _header
            /*
                why put `_header` under `_rows`?
                consider the initializing sequence, the item which is below gets initialized first. and we should make
                sure `__childrenWidthsManager` -- which under `_header` -- be initialized first, then the children of
                `_rows` can hook up with `_header` object.
             */
            anchors.left: parent.left
            anchors.top: parent.top
            height: LCGeometry.BarHeight
            z: 2

            Repeater {
                model: p_header

                delegate: LCRectangle {
                    id: _headerRect
                    height: parent.height
                    p_border.width: 1
                    p_radius: 0

                    property bool p_clickable: false
                    signal fn_clicked

                    LCText {
                        id: _headerTxt
                        anchors.centerIn: parent
                        p_text: modelData
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (p_clickable) {
                                parent.fn_clicked()
                            }
                        }
                    }

                    Component.onCompleted: {
                        const preferredWidth = _headerTxt.width + LCGeometry.HSpacingM * 2
                        _headerRect.width = preferredWidth
                        __childrenWidthsManager[model.index] = _headerRect
                        fn__updateContentWidth(0, preferredWidth)
                        // after this component completed, the `__childrenWidthsManager` got initialized, too.
                        // console.log("LCTable.qml:141#_headerRect", '__childrenWidthsManager initialized')
                    }
                }
            }
        }
    }

    // -------------------------------------------------------------------------
    // shift + mouse-wheel to horizontal scroll
    //      https://stackoverflow.com/questions/54609620/how-to-use-the-scroll-on-a-horizontal-qml-scrollview

    MouseArea {
        anchors.fill: parent

        onWheel: {
            if (wheel.modifiers & Qt.ShiftModifier) {
                if (wheel.angleDelta.y > 0) {
                    _root.ScrollBar.horizontal.decrease()
                } else {
                    _root.ScrollBar.horizontal.increase()
                }
            }
        }

        // and pass other mouse events to the children
        onClicked: mouse.accepted = false
        onDoubleClicked: mouse.accepted = false
        onPositionChanged: mouse.accepted = false
        onPressAndHold: mouse.accepted = false
        onPressed: mouse.accepted = false
        onReleased: mouse.accepted = false
    }
}
