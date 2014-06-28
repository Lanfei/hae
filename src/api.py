import os
import re
import assets
import webbrowser
from file import File
from menu import Menu
from menu import MenuItem
from process import Process
from trayicon import TrayIcon
from filedialog import FileDialog
from downloader import Downloader
from socketserver import SocketServer
from socketclient import SocketClient
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QObject, pyqtSlot

class API(QObject):

	def __init__(self, parent):
		super(API, self).__init__(parent)
		self.window = parent

	# Slots

	# 获取版本号
	@pyqtSlot(result = str)
	def version(self):
		return assets.version

	# 获取Manifest
	@pyqtSlot(str, result = str)
	def manifest(self, name, default = ''):
		return assets.manifest[name] if name in assets.manifest else default

	# 根据当前页面获取URL
	@pyqtSlot(str, result = str)
	def normUrl(self, url):
		p = re.compile('(^file:\/\/)|(^http:\/\/)|(^https:\/\/)|(^data:)')
		if url and p.match(url) == None:
			url = os.path.normpath(os.path.dirname(self.window.webView.url().toLocalFile()) + '/' + url)
		return url

	# 打开浏览器
	@pyqtSlot(str)
	def browse(self, url):
		webbrowser.open(url)

	# 保存本地数据
	@pyqtSlot(str, str)
	def setData(self, name, value):
		assets.dataJar.set(name, value)

	# 获取本地数据
	@pyqtSlot(str, result = str)
	def getData(self, name):
		return assets.dataJar.get(name)

	# 删除本地数据
	@pyqtSlot()
	@pyqtSlot(str)
	def removeData(self, name = None):
		return assets.dataJar.remove(name)

	# 关闭所有窗口
	@pyqtSlot()
	def closeAllWindows(self):
		QApplication.closeAllWindows()

	# TODO 清除缓存
	@pyqtSlot()
	def clearCaches(self):
		pass

	# Factories

	# 窗口
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, int, result = QObject)
	@pyqtSlot(str, int, int, result = QObject)
	def createWindow(self, url = '', width = None, height = None):
		from window import Window
		return Window(self.window, self.normUrl(url), width, height)

	# 对话框
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, int, result = QObject)
	@pyqtSlot(str, int, int, result = QObject)
	def createDialog(self, url = '', width = None, height = None):
		from window import Window
		return Window(self.window, self.normUrl(url), width, height, True)

	# 文件选择对话框
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, str, result = QObject)
	def createFileDialog(self, caption = '', directory = ''):
		return FileDialog(self.window, caption, directory)

	# 菜单
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	def createMenu(self, title = '', icon = ''):
		return Menu(self.window, title, self.normUrl(icon))

	# 菜单项
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, str, result = QObject)
	@pyqtSlot(str, str, bool, result = QObject)
	def createMenuItem(self, text, icon = '', checkable = False):
		return MenuItem(self.window, text, self.normUrl(icon), checkable)

	# 托盘图标
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, str, result = QObject)
	def createTrayIcon(self, toolTip = '', icon = ''):
		return TrayIcon(self.window, toolTip, self.normUrl(icon))

	# 文件对象
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, str, result = QObject)
	@pyqtSlot(str, str, str, result = QObject)
	def createFile(self, filename, mode = 'r', encoding = 'utf-8'):
		return File(self.window, filename, mode, encoding)

	# 文件下载
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, str, result = QObject)
	@pyqtSlot(str, str, bool, result = QObject)
	def createDownloader(self, url, filename = None, resume = False):
		return Downloader(self.window, url, filename, resume)

	# 子进程
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	def createProcess(self, encoding = None):
		return Process(self.window, encoding)

	# 套接字服务端
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	@pyqtSlot(str, int, result = QObject)
	def createSocketServer(self, encoding = 'utf-8', timeout = None):
		return SocketServer(self.window, encoding, timeout)

	# 套接字客户端
	@pyqtSlot(result = QObject)
	@pyqtSlot(str, result = QObject)
	def createSocketClient(self, encoding = 'utf-8'):
		return SocketClient(self.window, encoding)
