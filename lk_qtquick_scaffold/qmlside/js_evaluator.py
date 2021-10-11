from PySide6.QtQml import QQmlComponent
from lk_logger import lk

from ..typehint import TJsEvaluatorCore
from ..path_model import qmlside_dir


class JsEvaluator:
    core: TJsEvaluatorCore
    
    def __init__(self):
        from ..pyside import app
        component = QQmlComponent(app.engine, f'{qmlside_dir}/view.qml')
        qobject = component.create()
        self.core = qobject
        lk.log(self.core.test())
    
    def bind_anchors(self, a_obj, a_prop, b_obj, b_prop):
        self.eval_js('{{0}}.{} = Qt.binding(() => {{1}}.{})'.format(
            a_prop, b_prop
        ), a_obj, b_obj)
    
    def eval_js(self, code, *args):
        lk.loga(code, len(args), h='parent')
        return self.core.eval_js(
            code.format(*(f'args[{i}]' for i in range(len(args)))),
            list(args)
        )


js_eval = JsEvaluator()
