from __future__ import annotations

if __name__ == '__main__':
    from ...application import Application


def init(app: 'Application'):
    from .listview import ListView
    from .slider import Slider
    from .util import Util
    
    app.register(ListView(), 'PyListView')
    app.register(Slider(), 'PySlider')
    app.register(Util(), 'PyUtil')
