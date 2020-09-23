import QtQuick 2.14
import QtQuick.Controls 2.14
import "./LCStyle/geometry.js" as LCGeometry

ScrollView {
    id: _root
    contentWidth: _row.width; contentHeight: _row.height
    wheelEnabled: true

    property int p_cellWidthMax: LCGeometry.BarWidth
    property var p_dataA  // {field: list values}  // suggest
    property var p_dataB  // [list row_values, ...]  // not suggest
    property var p_delegates: Object()  // {colx: CellComponent}  // FIXME: this is experimental property
    property var p_header  // [str field, ...]
    property var __data: Object()
    //      [list col_values, ...], you can use `__data[0][1]` to fetch (2nd row, 1st col)'s cell value.
    property int __cellHeight: LCGeometry.BarHeight

    onP_dataAChanged: {
        let colx
        for (let field in p_dataA) {
            colx = p_header.indexOf(field)
            __data[colx] = p_dataA[field]
        }
    }

    onP_dataBChanged: {
        for (let rowx in p_dataB) {
            for (let colx in p_dataB[rowx]) {
                __data[colx][rowx] = p_dataB[rowx][colx]
                //     ^ x   ^ y
            }
        }
    }

    function fn_minimalCellsUpdate(data) {
        // data: [(rowx, colx, value), ...]
        let rowx, colx, value
        for (let i in data) {
            rowx = data[i][0]
            colx = data[i][1]
            value = data[i][2]
            __data[colx][rowx] = value
            //     ^ x   ^ y
        }
    }

    Row {  // horizontal linear constraint
        id: _row
        height: parent.height
        // width: __cellHeight * __data.length
        //      while width matches children content width. or: `width = __cellHeight * __data.length`

        // each field corresponds to a ListView, we create multiple ListView components based on `p_header`.
        // each ListView is draggable to change their widths. but the line height is fixed.
        Repeater {
            id: _repeater
            model: p_header

            delegate: ListView {
                // TODO: drag the right edge to resize ListView's width.
                id: _list
                objectName: "LCTable.qml#_list" + p_colx
                model: __data[p_colx]  // -> [value1, value2, ...]
                width: LCGeometry.ButtonWidthM
                property string p_title: modelData  // provided by parent (Repeater)
                property int p_colx: p_header.indexOf(modelData)

                delegate: {
                    if (p_delegates[p_colx]) {
                        return p_delegates[p_colx]
                    } else {
                        return _defaultCell
                    }
                }

                Component.onCompleted: {
                    _list.height = childrenRect.height
                    console.log("LCTable.qml:78", p_colx, _list.model,
                                [_list.width, _list.height], )
                }
            }
        }

        Component {
            id: _defaultCell
            LCRectangle {
                id: _cell
                width: parent.parent.width; height: __cellHeight
                //     ^ `parent.parent` points to ListView
                p_border.width: 1
                p_radius: 0

                property bool p_clickable: false
                signal fn_clicked

                LCText {
                    id: _txt
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
                    // console.log("LCTable.qml:112", parent, parent.parent)
                    // //                             ^ QQuickItem (don't know who it is)
                    // //                                     ^ this is ListView

                    let preferredWidth = _txt.width + LCGeometry.HSpacingM * 2
                    if (preferredWidth > p_cellWidthMax) {
                        preferredWidth = p_cellWidthMax
                    }

                    if (preferredWidth > parent.parent.width) {
                        parent.parent.width = preferredWidth
                    }

                    // console.log("LCTable.qml:125",
                    //             preferredWidth,
                    //             _cell.width, _cell.height,
                    //             parent.parent.width, parent.parent.height)
                }
            }
        }
    }

    MouseArea {
        // shift + mouse-wheel to horizontal scroll
        //      https://stackoverflow.com/questions/54609620/how-to-use-the-scroll-on-a-horizontal-qml-scrollview
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

    Component.onCompleted: {
        // console.log("LCTable.qml:159",
        //             [_root.width, _root.height],
        //             [_root.contentWidth, _root.contentHeight],
        //             [_row.width, _row.height],)
    }
}