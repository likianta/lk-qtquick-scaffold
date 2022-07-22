from __future__ import annotations

import typing as t

from .register import PyRegister
from ..qt_core import QObject
from ..qt_core import slot


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
    def eval(self, code: str, kwargs: dict = None) -> t.Any:
        from textwrap import dedent, indent
        # print(':l', kwargs, '\n' in code)
        # print(code)
        
        if kwargs is None: kwargs = {}
        kwargs.update({'__file__': __file__})
        
        code_wrapper = dedent('''
            def __selfunc__():
                # the source code can use `__selfunc__` for recursive call.
                {source_code}
            __return_hook__ = __selfunc__()
        ''').format(source_code=indent(dedent(code), '    '))
        exec(code_wrapper, kwargs)
        
        print(kwargs['__return_hook__'])
        return kwargs['__return_hook__']
    
    @slot(str, name='def')
    def def_(self, code_block: str) -> None:
        import re
        from textwrap import dedent
        code_block = dedent(code_block)
        funcname = re.search('^def (\w+)', code_block).group(1)
        code_wrapper = dedent('''
            {source_code}
            __func_hook__ = {funcname}
        ''').format(source_code=code_block, funcname=funcname)
        exec(code_wrapper, hook := {})
        self.register(hook['__func_hook__'], name=funcname)
    
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


pyside = PySide()
register = pyside.register_via_decorator
