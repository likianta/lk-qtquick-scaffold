"""
usage:
    run in command line:
        py -m lk_qtquick_scaffold -h
        py -m lk_qtquick_scaffold run <qml_file>
        py -m lk_qtquick_scaffold run <qml_file> --debug
        ...
"""
from argsense import cli


@cli.cmd()
def run(view: str, debug=False):
    """
    args:
        view: the qml file (relative or absolute path) to load.
    """
    from lk_qtquick_scaffold import app
    app.run(view, debug=debug)


@cli.cmd()
def list_builtin_pyhandlers():
    """
    list:
        # if you see multiple keywords in a line below (separated by comma),
        # they mean candidate words.
        # the candidates are not registered into qml side, but only reserved
        # here.
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
    # list_ = (
    #     'pyside',
    #     'pystyle',
    #     'pyalign',
    #     'pycolor',
    #     'pyfont',
    #     'pymotion',
    #     'pysize',
    #     'pylayout',
    #     'pyrss',
    # )
    # print(':ls', list_)
    print('''
        - pyside
        - pystyle
            - pycolor
            - pyfont
            - pymotion
            - pysize
        - pyalign
        - pycolor
        - pyfont
        - pymotion
        - pysize
        - pylayout
        - pyrss
    ''')


if __name__ == '__main__':
    cli.run()
