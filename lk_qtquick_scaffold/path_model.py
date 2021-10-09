from os.path import dirname

curr_dir = dirname(__file__).replace('\\', '/')
pkg_dir = curr_dir
proj_dir = dirname(pkg_dir)

theme_dir = f'{pkg_dir}/theme'
