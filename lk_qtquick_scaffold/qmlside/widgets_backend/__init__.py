from __future__ import annotations

if __name__ == '__main__':
    from ...application import Application


def init(app: 'Application'):
    from .slider import Slider
    app.register(Slider(None), 'PySlider')
