import QtQuick 2.15

Text {
    id: root
    objectName: 'LayoutHelper'
    font.pixelSize: 12

    function get_content_size(text, pixel=12) {
        root.font.pixelSize = pixel
        return root.contentWidth
    }
}
