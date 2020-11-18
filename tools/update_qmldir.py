from lk_utils import filesniff

dir0 = '../lk_qtquick_scaffold/qml/LightClean'

for d in (dir0, f'{dir0}/LCButtons', f'{dir0}/LCStyle',):
    qml_files = filesniff.findall_files(d, 'dict', suffix='.qml')
    
