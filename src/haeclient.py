#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import codecs
import assets
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QTranslator

class HAEClient:
	def __init__(self):
		from codec import Codec
		from window import Window
		from system import System
		from datajar import DataJar
		from filesystem import FileSystem

		try:
			manifest = json.load(codecs.open('manifest.json', 'r', 'utf-8'))
		except:
			manifest = {}

		for key in assets.manifest:
			if key in manifest:
				assets.manifest[key] = manifest[key]

		self.app = QApplication(sys.argv)
		self.app.setApplicationName(assets.manifest['name'])
		self.app.setApplicationVersion(assets.manifest['version'])

		assets.sys = System()
		assets.codec = Codec()
		assets.fs = FileSystem()
		assets.dataJar = DataJar()

		translator = QTranslator()
		if translator.load("zh_CN.qm"):
			self.app.installTranslator(translator)

		self.window = Window(None, assets.manifest['path'] + 'index.html')

		sys.exit(self.app.exec_())

if __name__ == '__main__':
	HAEClient()
