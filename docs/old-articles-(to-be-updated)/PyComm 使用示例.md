# 子类继承自 PyComm

```python
# control.py
from lk_qtquick_scaffold.pycomm import PyHandler


class FileFinder(PyHandler):

    def get_files(self):
        pass


finder = FileFinder()  # The finder has automatically been registered in Qml (as 
#   name of 'FileFinder') when you instantiate it.

```

```qml
// view.qml
import QtQuick 2.0

Item {
    Component.onCompleted: {
        const files = FileFinder.call('get_files')
    }
}

```

# 自定义注册到 Qml 的对象名称

```python
# control.py
from lk_qtquick_scaffold.pycomm import PyHandler


class FileFinder(PyHandler):

    def __init__(self, home_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.home_dir = home_dir

    def get_files(self):
        pass  # Here used self.home_dir...


finder1 = FileFinder('A/B', object_name='Finder1')  
finder2 = FileFinder('A/C', object_name='Finder2')
#                           ^-------------------^
#   The `object_name` defines what you can use in Qml context. The default name
#   is FileFinder's class name.

```

```qml
// view.qml
import QtQuick 2.0

Item {
    Component.onCompleted: {
        const files1 = Finder1.call('get_files')
        const files2 = Finder2.call('get_files')
        //             ^-----^
        //  Use registered class name like this.
    }
}

```



