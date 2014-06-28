from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QFileDialog

class FileDialog(QFileDialog):

	def __init__(self, parent, caption = '', directory = ''):
		super(FileDialog, self).__init__(parent, caption, directory)

	# 设置对话框标题
	@pyqtSlot(str)
	def setCaption(self, caption):
		self.setWindowTitle(caption)

	# 设置对话框目录
	@pyqtSlot(str)
	def setDirectory(self, directory):
		super(FileDialog, self).setDirectory(directory)

	# 设置打开、保存模式
	# AcceptMode {0: AcceptOpen, 1: AcceptSave}
	@pyqtSlot(int)
	def setAcceptMode(self, acceptMode):
		super(FileDialog, self).setAcceptMode(acceptMode)

	# 设置文件选择模式
	# FileMode {0: AnyFile, 1: ExistingFile, 2: Directory, 3: ExistingFiles, 4: DirectoryOnly}
	@pyqtSlot(int)
	def setFileMode(self, fileMode):
		super(FileDialog, self).setFileMode(fileMode)

	# 设置默认保存扩展名
	@pyqtSlot(str)
	def setDefaultSuffix(self, defaultSuffix):
		super(FileDialog, self).setDefaultSuffix(defaultSuffix)

	# 设置默认选中文件
	@pyqtSlot(str)
	def selectFile(self, filename):
		super(FileDialog, self).selectFile(filename)

	# 选中过滤器
	@pyqtSlot(str)
	def setFilters(self, filters):
		self.setNameFilter(filters)

	# 添加过滤器
	@pyqtSlot(str)
	def addFilter(self, newFilter):
		filters = self.nameFilters()
		filters.append(newFilter)
		self.setNameFilters(filters)

	# 设置默认过滤器
	@pyqtSlot(str)
	def selectFilter(self, defFilter):
		self.selectNameFilter(defFilter)

	# 显示文件选择对话框
	@pyqtSlot(result = str)
	def exec(self):
		if(super(FileDialog, self).exec()):
			return '\n'.join(self.selectedFiles())
		return ''
