# -*- coding: utf-8 -*-import sys
import sys, assets
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
	base = 'Win32GUI'

options = {
	'build_exe': {
		'includes': [
			'atexit',
			'PyQt5.Qt',
			'PyQt5.QtCore',
			'PyQt5.QtWebKit',
			'PyQt5.QtWidgets',
			'PyQt5.QtPrintSupport'
		],
		'include_files': [
			'../assets',
			'plugins/iconengines',
			'plugins/mediaservice',
			'qt.conf',
			'manifest.json'
		],
		'icon': 'icon.ico'
	}
}

executables = [
	Executable('haeclient.py', base=base)
]

setup(
	name = assets.manifest['name'],
	version = assets.manifest['version'],
	description = assets.manifest['description'],
	options = options,
	executables = executables
)
