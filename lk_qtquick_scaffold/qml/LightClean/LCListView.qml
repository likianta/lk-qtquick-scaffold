import QtQuick 2.14

Item {
    property alias obj_ListView: _list

    LCListModel {
        id: _model
    }

    ListView {
        id: _list
        model: _model
    }
}