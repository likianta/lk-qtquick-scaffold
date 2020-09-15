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
