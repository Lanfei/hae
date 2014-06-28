from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.Qt import QSystemTrayIcon, QIcon

class TrayIcon(QSystemTrayIcon):

	ActivationReason = ['Unknown', 'Context', 'DoubleClick', 'Trigger', 'MiddleClick']

	onactivate		 = pyqtSignal(int, str)
	onmessageclick	 = pyqtSignal()

	def __init__(self, parent, toolTip = '', icon = ''):
		super(TrayIcon, self).__init__(parent)
		self.setObjectName('trayIcon')
		self.setIcon(icon)
		self.setToolTip(toolTip)
		self.activated.connect(self.activateHandler)
		self.messageClicked.connect(self.onmessageclick)

	# Slots

	# 设置工具提示
	@pyqtSlot(str)
	def setToolTip(self, toolTip):
		super(TrayIcon, self).setToolTip(toolTip)

	# 设置图标
	@pyqtSlot(str)
	def setIcon(self, icon):
		if icon:
			icon = QIcon(icon)
		else:
			icon = self.parent().windowIcon()
		super(TrayIcon, self).setIcon(QIcon(icon))

	# 设置右键菜单
	@pyqtSlot(QObject)
	def setContextMenu(self, menu):
		super(TrayIcon, self).setContextMenu(menu)

	# 获取是否可见
	@pyqtSlot(result = bool)
	def isVisible(self):
		return super(TrayIcon, self).isVisible()

	# 获取是否支持消息弹泡
	@pyqtSlot(result = bool)
	def supportsMessages(self):
		return super(TrayIcon, self).supportsMessages()

	# 获取是否支持系统托盘图标
	@pyqtSlot(result = bool)
	def isSystemTrayAvailable(self):
		return super(TrayIcon, self).isSystemTrayAvailable()

	# 显示托盘消息
	# showMessage

	# 设置可见性
	# setVisible

	# 显示
	# show

	# 隐藏
	# hide

	# Sinals

	def activateHandler(self, reason):
		self.onactivate.emit(reason, TrayIcon.ActivationReason[reason])
