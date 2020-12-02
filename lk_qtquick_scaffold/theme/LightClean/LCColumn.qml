import QtQuick 2.15
import "./LCStyle/dimension.js" as LCDimension
import "../../qml_helper/layout_helper.js" as LCLayout

Column {
    id: root
    padding: LCDimension.Padding
    spacing: LCDimension.VSpacingM

    property bool  p_alignCenter: false
    property bool  p_enableFillRest: false  // See `LCRow.p_autoWidth`
    property bool  p_fillWidth: false
    property alias p_padding: root.padding
    property alias p_spacing: root.spacing
    property real  r_fillRest: 0  // related to `p_enableFillRest`
    property real  __appliedHeight: {  // related to `p_enableFillRest`
        return (root.topPadding + root.bottomPadding) +
            (root.spacing * (root.children.length - 0))
    }

    // -------------------------------------------------------------------------

    function _updateFillWidth() {
        for (let i in root.children) {
            root.children[i].width = root.width -
                root.leftPadding -
                root.rightPadding
        }
    }

    function _updateFillRest() {
        root.r_fillRest = root.height - __appliedHeight
    }

    function _initAppliedHeight() {
        for (let i in root.children) {
            __appliedHeight += root.children[i].height
        }
        if (__appliedHeight < root.height) {
            return true
        } else {
            return false
        }
    }

    Component.onCompleted: {
        if (p_alignCenter) {
            for (let i in root.children) {
                root.children[i].anchors.horizontalCenter = root.horizontalCenter
            }
        }
        if (p_enableFillRest) {
            if (_initAppliedHeight()) {
                _updateFillRest()
                this.heightChanged.connect(_updateFillRest)
            }
        }
        if (p_fillWidth) {
            _updateFillWidth()
            this.widthChanged.connect(_updateFillWidth)
        }
    }
}
