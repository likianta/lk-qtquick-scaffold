import QtQuick 2.15
import QtGraphicalEffects 1.15
import LKDebugger 1.0
import LKHelper  1.0
import LightClean 1.0
import LightClean.LCButtons 1.0

LCWindow {
    id: root
    objectName: 'view#root'
    color: '#eeeeee'  // f2f2f2 | eeeeee
    visible: true
    width: 600; height: 800

    property string p_imgFile: ''

    LCColumn {
        id: _container
        objectName: 'view#_container'
        anchors {
            fill: parent
            margins: 20
        }
        clip: true

        LCRow {
            width: parent.width
            height: 160

            p_enableFillRest: true
            p_fillHeight: true

            LCRectangle {
                id: _profile
                objectName: 'view#_profile'
                width: parent.r_fillRest * 0.5
                p_color: 'transparent'

                LCColumn {
                    anchors {
                        fill: parent
                    }
                    LCText {
                        p_color: '#065FFA'
                        p_text: 'https://uimovement.com'
                    }
                    LCText {
                        p_alignment: 'ltop'
                        p_bold: true
                        p_color: '#333333'
                        p_size: 32
                        p_text: 'Where the master\npiece derived...'
                    }
                }
            }

            Loader {
                id: _miniCard
                objectName: 'view#_miniCard'
                width: parent.r_fillRest * 0.5
                // sourceComponent: _imgCard

                Component.onCompleted: {
                    // 注意: this.onCompleted 与 this.xChanged 的时机是不同的: 当
                    // this.onCompleted 发生时, this.x 还不正常; 当 this.xChanged
                    // 发生时 (这是一个瞬发信号), this.x 才是正确的.
                    // 我们需要把 this.x 正确时的那一刻的 x 和 y 位置, 初始化给
                    // _fullCard, 二者使用 connect 实现, 如下.
                    this.xChanged.connect(_fullCard.initLocation)
                }
            }
        }

        Rectangle {
            id: _ruler
            // anchors.top: _container.bottom
            // anchors.topMargin: 10
            width: 260
            height: 5
            color: '#EEDE25'
        }
    }

    Component {
        id: _imgCard

        LCRectangle {
            id: _imgFrame
            // width: parent.r_fillRest * 0.5
            // clip: true
            p_color: '#234471'

            layer.enabled: true  // true|false
            layer.effect: OpacityMask {
                maskSource: Rectangle {
                    width: _imgFrame.width
                    height: _imgFrame.height
                    radius: _imgFrame.radius
                }
            }

            Image {
                id: _img
                anchors {
                    // centerIn: parent
                    horizontalCenter: parent.horizontalCenter
                }
                // width: parent.width
                height: parent.height + p_floatingOffset
                fillMode: Image.Pad
                source: p_imgFile
                visible: true

                property bool p_hovered: _area.containsMouse
                property bool p_expanded: false
                property int  p_floatingOffset: 30

                function switchFloatable() {
                    _img.p_expanded = !_img.p_expanded
                }

                states: [
                    State {
                        when: _img.p_hovered & !_img.p_expanded
                        PropertyChanges {
                            target: _img
                            y: _imgFrame.y - p_floatingOffset
                            // height: _imgFrame.heigth + 20
                        }
                    }
                ]

                transitions: [
                    Transition {
                        NumberAnimation {
                            duration: 1000
                            easing.type: Easing.OutQuart
                            properties: "y"
                        }
                    },
                    Transition {
                        AnchorAnimation {
                            duration: 3000
                            easing.type: Easing.OutQuart
                            // properties: "width,height,x,y"
                        }
                    }
                ]
            }

            MouseArea {
                // When the mouse hovered, floating background image
                id: _area
                anchors.fill: parent
                hoverEnabled: true

                Component.onCompleted: {
                    this.clicked.connect(_fullCard.expand)
                    this.clicked.connect(_img.switchFloatable)
                }
            }
        }
    }

    Loader {
        id: _fullCard
        // anchors.fill: parent
        x: __initX
        y: __initY
        z: 1
        width: _miniCard.width
        height: _miniCard.height
        sourceComponent: _imgCard

        property bool p_show: false
        property int  __initX: 0
        property int  __initY: 0

        function initLocation() {
            // 注意: _miniCard.onCompleted 时, 它的位置是错误的 (x=0, y=0); 当
            // _miniCard.xChanged 时, 它的位置才是正确的 (x=280, y=0).
            const coord = _miniCard.mapToItem(null, 0, 0)
            _fullCard.__initX = coord.x
            _fullCard.__initY = coord.y
            Logger.log(coord.x, coord.y)
        }

        function expand() {
            _fullCard.p_show = !_fullCard.p_show
        }

        states: [
            State {
                when: _fullCard.p_show
                PropertyChanges {
                    target: _fullCard
                    width: root.width + 10
                    //  root.width + 10 | _root.width | _container.width
                    height: root.height + 10
                    //  root.height + 10 | _root.height | _container.height
                    x: -5  // -5 | 0 | _container.x
                    y: -5  // -5 | 0 | _container.y
                    /*        ^A   ^B  ^C
                        A: 可以避免 _imgMask 的圆角与 root 窗口的锋利边角产生的不和谐,
                           不过图片外围需要被稍微裁剪一圈
                        B: 不能避免 A 的情况, 这是最开始的设计
                        C: 覆盖 _container 的区域显示, 作为 A 的替代方法
                     */
                }
            }
        ]

        transitions: [
            Transition {
                NumberAnimation {
                    duration: 600
                    easing.type: Easing.OutQuart // InOutQuad | OutQuart
                    properties: 'width, height, x, y'
                }
            }
        ]
    }

    Component.onCompleted: {
        this.p_imgFile = './assets/test_img.jpg'
    }
}
