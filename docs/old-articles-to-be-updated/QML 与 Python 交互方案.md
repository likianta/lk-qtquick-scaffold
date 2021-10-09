# QML 调用 Python 方法

TODO

# Python 调用 QML 方法 (修改 QObject 属性)

TODO

# 注意事项

## 调用方法, 而不直接修改属性

```qml
// Do
Item {
    Button {
        onClicked: PyHooks.set('listview', _listview)
    }
    ListView {
        id: _listview
    }
}

// Do Not
Item {
    Button {
        onClicked: PyHooks.get('listview') = _listview
    }
    ListView {
        id: _listview
    }
}
```

```python
# Do
pyhooks.get('listview').update('model', ['a', 'b', 'c'])

# Do Not
pyhooks.get('listview')['model'] = ['a', 'b', 'c']
```

## QML 需预先绑定到 PyHooks, Python 才能获取

提供两种绑定方法:

**1. 手动绑定**

```qml
Item {
    id: _item
    Component.onCompleted: {
        PyHooks.set("SomePath/ThisComp.qml#_item", _item)
    }
}
```

缺点: 写起来比较麻烦.

**2. 自动绑定 (待实现@2020-09-15)**

```qml
Item {
    id: _item
    objectName: "SomePath/ThisComp.qml#_item"  // 一定要有该属性, 且值在全局唯一.

    // 对所有要绑定的组件, 填写 objectName 属性. 在布局生成后, PyHooks 会自动查
    // 找 QML 引擎中所有含有 objectName 属性的组件, 并添加到 PyHooks.hooks 字典
    // 中.
}
```

缺点: 动态组件绑定麻烦.

