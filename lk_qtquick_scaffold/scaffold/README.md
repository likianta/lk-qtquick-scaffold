# 主题的组织形式

基于目录结构讲解:

```
|- lk_qtquick_scaffold
    |- scaffold  # 脚手架只提供基于 QML 组件封装的 LK QML 组件, 为区分于 QML 组
    |            # 件, LK QML 组件名以 'LK' 开头
        |- widgets  # LK QML 组件库
            |- LKButtons  # 组件库内也有子文件夹, 须保证每个文件夹都有一个 
            |             # 'qmldir' (无后缀名) 文件
                |- LKBaseButton.qml
                |- LKButton.qml
                |- LKCheckBox.qml
                |- LKFlatButton.qml
                |- ...
                |- qmldir
            |- LKCheckList.qml  # 每个组件皆以 'LK' 开头. 在外部导入该组件时, 方
            |                   # 式为: 
            |                   #   // my_prj/qml/view.qml
            |                   #   import LKWidget
            |                   #   import LKWidget.LKButtons
            |                   #   
            |                   #   LKWindow {
            |                   #       LKRectangle {
            |                   #           anchors.fill: parent
            |                   #           LKText {
            |                   #               anchors.centerIn: parent
            |                   #               text: 'Hello'
            |                   #           }
            |                   #           LKButton {
            |                   #               text: 'Click'
            |                   #               onClicked: {
            |                   #                   console.log('Click!')
            |                   #               }
            |                   #           }
            |                   #       }
            |                   #   }
            |- LKColumn.qml
            |- LKDividerLine.qml
            |- LKEdit.qml
            |- ...
            |- qmldir
        |- theme  # 主题样式库. 主题样式库包含多个主题, 每个主题定义了各自的形
        |         # 状, 动效规格, 颜色, 字体排版等效果. 主题之间有明显差异化, 但
        |         # 它们共用一套 widgets.
            |- LightClean  # 已有的主题样式. 文件夹以大驼峰方式命名, 里面是 js 
            |              # 文件和一个 qmldir 文件
                |- dimension.js
                |- motion.js
                |- palette.js
                |- qmldir
                |- shape.js
                |- typography.js
            |- ...
    |- tools
        |- theme_designer  # 主题设计器, 提供一个可视化界面, 用于创作自己的主题,
        |                  # 导出的结果以类似于 '../scaffold/theme' 的形式保存
            |- qml
                |- view.qml
                |- ...
            |- launch.py  # 主题设计器从这里启动
            |- main.py
```
