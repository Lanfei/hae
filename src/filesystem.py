import os
import sys
import shutil
import assets
from PyQt5.Qt import QStandardPaths, QUrl
from PyQt5.QtCore import QObject, pyqtSlot

class FileSystem(QObject):

	# 读取目录内容
	@pyqtSlot(result = str)
	@pyqtSlot(str, result = str)
	def listDir(self, dirname = '.'):
		try:
			return '\n'.join(os.listdir(dirname))
		except:
			return ''

	# 获取资源目录
	@pyqtSlot(result = str)
	def resourcesPath(self):
		return assets.manifest['path']

	# 获取桌面目录
	@pyqtSlot(result = str)
	def desktopPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)

	# 获取文档目录
	@pyqtSlot(result = str)
	def documentsPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)

	# 获取字体目录
	@pyqtSlot(result = str)
	def fontsPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.FontsLocation)

	# 获取程序目录
	@pyqtSlot(result = str)
	def applicationsPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.ApplicationsLocation)

	# 获取音乐目录
	@pyqtSlot(result = str)
	def musicPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.MusicLocation)

	# 获取视频目录
	@pyqtSlot(result = str)
	def moviesPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)

	# 获取图片目录
	@pyqtSlot(result = str)
	def picturesPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)

	# 获取临时送文件目录
	@pyqtSlot(result = str)
	def tempPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.TempLocation)

	# 获取用户目录
	@pyqtSlot(result = str)
	def homePath(self):
		return QStandardPaths.writableLocation(QStandardPaths.HomeLocation)

	# 获取本应用程序数据目录
	@pyqtSlot(result = str)
	def dataPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.DataLocation)

	# 获取本应用程序缓存目录
	@pyqtSlot(result = str)
	def cachePath(self):
		return QStandardPaths.writableLocation(QStandardPaths.CacheLocation)

	# 获取应用程序数据目录
	@pyqtSlot(result = str)
	def genericDataPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation)

	# 获取应用程序缓存目录
	@pyqtSlot(result = str)
	def genericCachePath(self):
		return QStandardPaths.writableLocation(QStandardPaths.GenericCacheLocation)

	# 获取运行通信文件目录
	@pyqtSlot(result = str)
	def runtimePath(self):
		return QStandardPaths.writableLocation(QStandardPaths.RuntimeLocation)

	# 获取本应用程序配置文件目录
	@pyqtSlot(result = str)
	def configPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)

	# 获取应用程序配置文件目录
	@pyqtSlot(result = str)
	def genericConfigPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)

	# 获取下载目录
	@pyqtSlot(result = str)
	def downloadPath(self):
		return QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)

	# 获取绝对路径
	@pyqtSlot(result = str)
	@pyqtSlot(str, result = str)
	def absPath(self, path = ''):
		return os.path.abspath(path)

	# 格式化路径
	@pyqtSlot(result = str)
	@pyqtSlot(str, result = str)
	def normPath(self, path = ''):
		return os.path.normpath(path)

	# 获取网页用路径
	@pyqtSlot(result = str)
	@pyqtSlot(str, result = str)
	def localUrl(self, path = ''):
		return QUrl.fromLocalFile(path).toString()

	# 判断是否绝对路径
	@pyqtSlot(str, result = bool)
	def isAbsPath(self, path):
		return os.path.isabs(path)

	# 文件存在
	@pyqtSlot(str, result = bool)
	def isFile(self, filename):
		return os.path.isfile(filename)

	# 目录存在
	@pyqtSlot(str, result = bool)
	def isDir(self, dirname):
		return os.path.isdir(dirname)

	# 路径存在
	@pyqtSlot(str, result = bool)
	def exists(self, path):
		return os.path.exists(path)

	# 文件大小
	@pyqtSlot(str, result = int)
	def fileSize(self, filename):
		try:
			return os.path.getsize(filename)
		except:
			return -1

	# 创建文件
	@pyqtSlot(str, result = bool)
	def mkfile(self, filename):
		try:
			open(filename, 'w')
			return True
		except:
			return False

	# 创建目录
	@pyqtSlot(str, result = bool)
	def mkdir(self, dirname):
		try:
			os.mkdir(dirname)
			return True
		except:
			return False

	# 拷贝
	@pyqtSlot(str, str, result = bool)
	def copy(self, path1, path2):
		try:
			if os.path.isfile(path1):
				shutil.copy(path1, path2)
			else:
				shutil.copytree(path1, path2)
			return True
		except:
			return False

	# 移动文件
	@pyqtSlot(str, str, result = bool)
	def move(self, path1, path2):
		try:
			shutil.move(path1, path2)
			return True
		except:
			return False

	# 删除文件
	@pyqtSlot(str, result = bool)
	def remove(self, path):
		try:
			if os.path.isfile(path):
				os.remove(path)
			else:
				shutil.rmtree(path)
			return True
		except:
			return False

	# 在资源管理器中显示文件，只测试过Windows
	@pyqtSlot(str, result = bool)
	def explore(self, path):
		try:
			if sys.platform == 'darwin':
				os.popen('open --' + path)
			elif sys.platform == 'linux2':
				os.popen('gnome-open --' + path)
			elif sys.platform == 'win32':
				os.popen('explorer /select,' + path)
			return True
		except:
			return False
