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


if __name__ == '__main__':
    cli.run()
