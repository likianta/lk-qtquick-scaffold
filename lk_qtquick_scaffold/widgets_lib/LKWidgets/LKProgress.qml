import QtQuick 2.15

Item {
    id: root

    property bool   demoMode: false
    property int    precision: 0
    property string progColorBg: pycolor.prog_bg
    property string progColorFg: pycolor.prog_fg
    property alias  progWidth: _prog_bg.width
    property int    progHeight: 4
    property int    progRadius: progHeight / 2
    property real   progValue: 0  // 0.0 ~ 1.0
    property int    __padding: 4

    signal textClicked()

    LKRectangle {
        id: _prog_bg
        anchors {
            left: parent.left
            right: _display.left
            rightMargin: root.__padding
            verticalCenter: parent.verticalCenter
        }
        height: root.progHeight
        radius: root.progRadius
        color: root.progColorBg

        LKRectangle {
            id: _prog_fg
            anchors.left: parent.left
            width: parent.width * root.progValue
            height: parent.height
//            radius: parent.radius
            color: root.progColorFg

            Behavior on width {
                enabled: root.demoMode
                NumberAnimation {
                    duration: 200
                }
            }
        }
    }

    Loader {
        id: _test_prog
        enabled: root.demoMode
        anchors.fill: parent

        sourceComponent: MouseArea {
            anchors.fill: parent

            property var progress

            onClicked: {
                _test_timer.value = 0
                _test_timer.start()
            }

            Timer {
                id: _test_timer
                interval: 1
                repeat: true
                property real value: 0
                onTriggered: {
                    this.value += 1
                    if (this.value >= 100) {
                        this.stop()
                    }
                }
                Component.onCompleted: {
                    this.valueChanged.connect(() => {
                        progress.progValue = this.value / 100
                    })
                }
            }
        }

        onLoaded: {
            this.item.progress = root
        }
    }

    LKText {
        id: _display
        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }

        property real __value: root.progValue

        Behavior on __value {
            NumberAnimation {
                duration: 200
            }
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                root.textClicked()
            }
        }

        Component.onCompleted: {
            this.text = PySlider.show_value(100, root.precision)
            this.width = this.contentWidth
            this.__valueChanged.connect(() => {
                this.text = PySlider.show_value(this.__value, root.precision)
            })
            this.__valueChanged()
        }
    }
}
