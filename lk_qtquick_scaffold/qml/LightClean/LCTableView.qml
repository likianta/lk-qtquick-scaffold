import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.14
import "./LCStyle/geometry.js" as LCGeometry

TableView {
    id: _root

    property var p_delegate
    property alias p_header: _repeater.model  // [{role: str, title: str}, ...]
    property alias p_model: _root.model  // {str role: list values}

    delegate: p_delegate

    Repeater {
        id: _repeater
        delegate: TableViewColumn {
            delegate: p_delegate
            role: model.role
            title: model.title
        }
    }
}