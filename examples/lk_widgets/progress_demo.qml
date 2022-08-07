import LKWidgets 1.0

LKWindow {
    width: 400
    height: 200

    LKColumn {
        anchors.fill: parent
        anchors.margins: 24
        alignment: 'hcenter,hfill'
        autoSize: true

        LKProgressA {
            height: 0
            demoMode: true
        }

        LKProgressB {
            height: 0
            demoMode: true
            model: {
                0.0: 'low',
                0.5: 'medium',
                1.0: 'high',
            }
        }
    }
}
