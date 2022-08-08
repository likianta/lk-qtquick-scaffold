import QtQuick 2.15

Item {
    id: root
    width: pysize.bar_width
    height: pysize.bar_height

    property bool   demoMode: false
    property var    model
    property int    precision  // suggested 0 or 2
    property string progColorBg: pycolor.progress_bg
    property string progColorFg: pycolor.progress_fg
    property alias  progItem: _fg_loader.item
    property real   progValue: 0  // usually 0.0 ~ 1.0, allow overflows.
    property int    progWidth: 0
    property bool   showText: false
    property alias  textItem: _text_loader.item
    property var    __model
    property int    __spacing: pysize.spacing_l
    property string __progType: Boolean(model) ? 'B' : 'A'
    property real   __progValue  // 0.0 ~ 1.0

    ProgBg {
        id: _bg
        anchors.centerIn: parent
//        width: root.progWidth
        height: pysize.progress_height
        color: root.progColorBg

        Loader {
            id: _fg_loader
            anchors.fill: parent
            source: root.__progType == 'A' ? 'ProgFgA.qml' : 'ProgFgB.qml'

            onLoaded: {
                this.item.color = Qt.binding(() => root.progColorFg)
                if (root.__progType == 'A') {
                    this.item.value = Qt.binding(() => root.__progValue)
                } else {
                    root.__modelChanged.connect(() => {
                        this.item.totalSteps = pyside.eval(`
                            return len(model)
                        `, {'model': root.__model})
                    })
                    root.__progValueChanged.connect(() => {
                        this.item.step = pyside.eval(`
                            return min(
                                enumerate(model),
                                key=lambda x: abs(x[1] - value)
                            )[0]
                        `, {
                            'model': root.__model,
                            'value': root.__progValue
                        })
                    })
                }
            }
        }

        Component.onCompleted: {
            root.progWidthChanged.connect(() => {
                if (root.__progType == 'A') {
                    this.width = root.progWidth
                } else {
                    this.width = root.progWidth - pysize.dot_radius_active * 2
                    this.x = pysize.dot_radius_active
                }
            })
        }
    }

    Loader {
        id: _text_loader
        visible: root.showText
        anchors {
            left: _loader.right
            right: parent.right
            verticalCenter: parent.verticalCenter
            leftMargin: root.__spacing
        }
        clip: true
        source: root.__progType == 'A' ? 'TextTypeA.qml' : 'TextTypeB.qml'
        onLoaded: {
            this.item.value = Qt.binding(() => root.__progValue)
            if (root.__progType == 'A') {
                this.item.demoMode = Qt.binding(() => root.demoMode)
                this.item.precision = Qt.binding(() => root.precision)
            } else {
                this.item.model = Qt.binding(() => root.model)
            }
        }
    }

    Loader {
        id: _demo_area_loader
        visible: root.demoMode
        anchors.fill: parent
        source: root.__progType == 'A' ? 'DemoAreaA.qml' : 'DemoAreaB.qml'
        onLoaded: {
            root.progValue = Qt.binding(() => this.item.demoValue)
            if (root.__progType == 'A') {
                // pass
            } else {
                this.item.progWidth = Qt.binding(() => root.progWidth)
            }
        }
    }

    Component.onCompleted: {
        if (root.progWidth == 0) {
            if (root.showText) {
                root.progWidth = Qt.binding(() => {
                    return root.width
                        - root.textItem.maxContentWidth
                        - root.__spacing
                })
            } else {
                root.progWidth = Qt.binding(() => root.width)
            }
        }
        this.modelChanged.connect(() => {
            if (this.model) {
                this.__model = pyside.eval(`
                    return {round(float(k), 5): v
                            for k, v in model.items()}
                `, {'model': this.model})
            }
        })
        this.progValueChanged.connect(() => {
            this.__progValue = lkprogress.get_nearest_progress(
                this.progValue, this.__model
            )
        })
        this.modelChanged()
    }
}
