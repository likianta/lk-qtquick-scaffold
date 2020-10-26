参考: https://stackoverflow.com/questions/54695976/how-can-i-update-a-qml-objects-property-from-my-python-file

注意事项: 不能使用 `QObject.property`, `QObject.setProperty`, 只能使用 `QQmlProperty`.

```python
""" QML Snippet
Rectangle {
    id: _rect
    border.color: "red"
    border.width: 0
}
"""

def wrong1(rect):
    rect.setProperty('border.width', 2)  # 报错
    
def wrong2(rect):
    border = rect.property('border')
    border.setProperty('width', 2)
    
def right1(rect):
    from PySide2.QtQml import QQmlProperty
    border_width = QQmlProperty(rect, 'border.width')
    print(border_width.read())  # -> 0
    border_width.write(2)

def right2(rect):
    from PySide2.QtQml import QQmlProperty
    border = QQmlProperty(rect, 'border')
    border_width = QQmlProperty(border.read(), 'width')  # 注意这里写的是 `border.read()`, 不是 `border`
    print(border_width.read())  # -> 0
    border_width.write(2)

```