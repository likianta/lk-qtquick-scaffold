from __future__ import annotations

from qtpy.QtCore import QObject

from .register import PyRegister
from .signal_slot import slot


class PySide(QObject, PyRegister):
    
    @slot(str, result=object)
    @slot(str, list, result=object)
    @slot(str, list, dict, result=object)
    def call(self, func_name: str, args: list = (), kwargs: dict = None):
        """ call python functions in qml side. """
        func, narg = self._pyfunc_holder[func_name]  # narg: 'number of args'
        if kwargs:
            return func(*args, **kwargs)
        elif narg == 0:
            return func()
        elif narg == -1:  # see `PyRegister._get_number_of_args.<return>`
            return func(*args)
        else:
            if isinstance(args, list) and narg > 1:
                return func(*args)
            else:  # experimental feature.
                return func(args)
    
    @slot(str, result=object)
    @slot(str, dict, result=object)
    def eval(self, code, kwargs: dict = None):
        from lk_lambdex import lambdex
        # print(':v', kwargs, code)
        if kwargs is None:
            return lambdex('', code)()
        else:
            return lambdex(', '.join(kwargs.keys()), code)(*kwargs.values())
    
    @slot(result=list)
    def list_reserved_pyhandler_names(self) -> tuple[str, ...]:
        """
        list:
            # if you see multiple keywords in a line below (separated by comma),
            # they mean candidate words. the candidates are not registered into
            # qml side, but backuped in this docstring.
            pyside
            pystyle, pytheme
                pyalign     # from `pystyle.align`
                pycolor     # from `pystyle.color`
                pyfont      # from `pystyle.font`
                pymotion    # from `pystyle.motion`
                pysize      # from `pystyle.size`
            pylayout, pyctrl, pycontrol
            pyrss, pyresource
        """
        return (
            'pyside',
            'pystyle',
            'pyalign',
            'pycolor',
            'pyfont',
            'pymotion',
            'pysize',
            'pylayout',
            'pyrss',
        )


pyside = PySide()  # noqa
register = pyside.register_via_decorator
