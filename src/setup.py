# -*- coding: utf-8 -*-import sys
import sys
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
			'plugins',
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
	name = "Hybrid App Engine",
	version = '1.0.0',
	description = '轻量级的桌面Web应用程序引擎',
	options = options,
	executables = executables
)
