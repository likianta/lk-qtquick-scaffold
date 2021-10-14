from os.path import dirname

curr_dir = dirname(__file__).replace('\\', '/')
pkg_dir = curr_dir
proj_dir = dirname(pkg_dir)

pyside_dir = f'{pkg_dir}/pyside'
qmlside_dir = f'{pkg_dir}/qmlside'
theme_dir = f'{pkg_dir}/theme'

assets_dir = f'{theme_dir}/Assets'
