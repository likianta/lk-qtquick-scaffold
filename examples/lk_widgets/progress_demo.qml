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

        LKProgressA {
            height: 0
            demoMode: root.demoMode
        }

        LKProgressB {
            height: 0
            demoMode: root.demoMode
            model: {
                0.0: 'low',
                0.5: 'medium',
                1.0: 'high',
            }
        }

        LKProgressC {
            height: 0
            precision: 2
            progItem.demoMode: root.demoMode
        }

        LKProgressD {
            height: 0
            progItem.demoMode: root.demoMode
            model: {
                0.0: 'low',
                0.5: 'medium',
                1.0: 'high',
            }
        }
    }
}
