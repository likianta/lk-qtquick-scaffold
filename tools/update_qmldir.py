from lk_utils import filesniff

dir0 = '../lk_qtquick_scaffold/qml/LightClean'

for d in (dir0, f'{dir0}/LCButtons', f'{dir0}/LCStyle',):
    qml_files = {fp: fn for fp, fn in filesniff.find_files(d, '*.qml')}
