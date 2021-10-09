from PySide6.QtQml import QJSEngine

qjs_engine = QJSEngine()


def aligning(a, b):
    a_obj, a_anchor = a
    b_obj, b_anchor = b
    
    qjs_engine.evaluate('{}.{} = {}.{}')

