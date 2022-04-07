from lk_utils.read_and_write import read_lines
from lk_utils import filesniff

all_qml_files = filesniff.findall_file_paths(
    '../lk_qtquick_scaffold/qml/LightClean', 'dict', '.qml')


def main(text):
    for fp, fn in all_qml_files.items():
        for i, x in enumerate(read_lines(fp), 1):
            if text in x:
                print(f'{fp}:{i}', '>>', x)


if __name__ == '__main__':
    main('p_pressedColor')
