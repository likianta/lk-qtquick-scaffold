import LKWidget 1.0

LKWindow {

    LKRectangle {
        anchors.fill: parent

        LKColumn {
            id: _leftcol
            anchors.left: parent.left
            spacing: 10
            width: 200; height: parent.height
            // TODO
        }

        LKColumn {
            id: _rightcol
            anchors.left: _leftcol.right
            anchors.leftMargin: 20
            spacing: 10
            width: parent.width - _leftcol.width - 20; height: parent.height
            // TODO
        }
    }
}
