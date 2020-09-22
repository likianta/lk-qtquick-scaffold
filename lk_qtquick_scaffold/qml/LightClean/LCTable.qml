import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.14
import "./LCStyle/geometry.js" as LCGeometry

ScrollView {
    id: _root
    anchors.margins: LCGeometry.MarginM
    clip: true

    property var p_header  // [str title, ...]
    property var p_model  // [{title: value}, ...]. p_model[0].keys() == p_header
    property var p_widths: []  // [float, ...]. len(self) == len(p_header)
    property real __cellWidth

    Row {
        id: _header
        width: parent.width; height: LCGeometry.BarHeight

        Repeater {
            model: p_header
            delegate: LCRectangle {
                width: __cellWidth; height: parent.height
                p_border.width: 1
                p_radius: 0

                property bool p_clickable: false
                signal fn_clicked

                LCText {
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
            }
        }

        Component.onCompleted: {
            __cellWidth = _root.width / p_header.length
            // TODO: `p_widths` not ready to use.
            // if (p_widths.length == 0) {
            //     __cellWidth = _root.width / p_header.length
            // } else {
            //
            // }
        }
    }

    ListView {
        id: _rows
        // anchors.fill: parent
        anchors.top: _header.bottom
        orientation: ListView.Vertical
        spacing: 0
        width: parent.width; height: parent.height - _header.height

        model: p_model
        delegate: Row {
            id: _cols
            spacing: 0
            width: parent.width; height: LCGeometry.BarHeight

            property int p_index: model.index

            Repeater {
                id: _cells
                model: p_header
                delegate: LCRectangle {
                    id: _cell
                    clip: true
                    width: __cellWidth; height: parent.height

                    p_border.width: 1
                    p_radius: 0

                    property bool p_clickable: false
                    property string p_title
                    signal fn_clicked

                    LCText {
                        anchors.centerIn: parent
                        p_text: _rows.model[_cols.p_index][p_title]
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
                        console.log(
                            "LCTable.qml",
                            p_title,  // title
                            // model.index,  // repeater index
                            parent.p_index,  // rowx
                            _rows.model[parent.p_index][p_title]  // allData[rowx][title]
                        )
                        _cell.width = _cell.childrenRect.width
                    }
                }
            }
        }
    }
}
