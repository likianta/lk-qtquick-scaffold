import LKWidgets 1.0

LKWindow {
    id: root
    width: 400
    height: 600

    property bool demoMode: true

    LKColumn {
        anchors.fill: parent
        anchors.margins: 24
        alignment: 'hcenter,hfill'
        autoSize: true

        LKProgress {
            height: 0
            demoMode: root.demoMode
            showText: false
        }

        LKProgress {
            height: 0
            demoMode: root.demoMode
            showText: false
            model: {
                0.0: 'low',
                0.5: 'medium',
                1.0: 'high',
            }
        }

        LKProgress {
            height: 0
            demoMode: root.demoMode
            precision: 2
            showText: true
        }

        LKProgress {
            height: 0
            demoMode: root.demoMode
            showText: true
            model: {
                0.0: 'low',
                0.5: 'medium',
                1.0: 'high',
            }
        }
    }
}
