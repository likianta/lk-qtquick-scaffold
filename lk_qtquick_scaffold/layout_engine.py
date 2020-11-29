"""
@Author   : likianta (likianta@foxmail.com)
@FileName : layout_engine.py
@Version  : 0.1.0
@Created  : 2020-11-29
@Updated  : 2020-11-29
@Desc     :
"""
from .pycomm import adapt_type, PyHandler, QObjectDelegator as Delegator


class PyLayoutHelper(PyHandler):
    
    def __init__(self):
        super().__init__(object_name='PyLayoutHelper')
        #                            ^--------------^
        #   This name will be available in QML global namespace.
        
        self.register_pyfunc(self.align_children)
    
    @adapt_type
    def align_children(self, parent: Delegator, alignment: str):
        """ Align children to parent.horizontalCenter or verticalCenter.
        
        Args:
            parent
            alignment ('hcenter'|'vcenter'|native):
                native: 'horizontalCenter'|'verticalCenter'|'left'|'right'|
                        'top'|'bottom'
        
        Examples:
            // view.qml
            Item {
                Text { anchors.top: parent.top }
                Rectangle { anchors.bottom: parent.bottom }
                Component.onCompleted: {
                    PyLayoutHelper.align_children(this, 'hcenter')
                }
            }
        
        """
        if alignment == 'hcenter':
            alignment = 'horizontalCenter'
        elif alignment == 'vcenter':
            alignment = 'verticalCenter'
        
        for i in parent.children():
            i.anchors[alignment] = parent[alignment]
            #   E.g. i.anchors.horizontalCenter = parent.horizontalCenter


pylayout_helper = PyLayoutHelper()
