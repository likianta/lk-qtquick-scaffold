import QtQuick
import Qt5Compat.GraphicalEffects

Image {
    id: root

    property int radius: pysize.radius_m

    layer.enabled: radius != 0
    layer.effect: OpacityMask {
        maskSource: Rectangle {
            width: root.width
            height: root.height
            radius: root.radius
        }
    }
}
