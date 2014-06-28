import sys
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.Qt import QProcess

class Process(QProcess):

	ProcessState	= ['NotRunning', 'Starting', 'Running']
	ProcessError	= ['FailedToStart', 'Crashed', 'Timedout', 'WriteError', 'ReadError', 'Unknown']
	ExitStatus		= ['NormalExit', 'CrashExit']

	onstart			= pyqtSignal()
	onerror			= pyqtSignal(int, str)
	onstatechange	= pyqtSignal(int, str)
	onstdout		= pyqtSignal(str)
	onstderr		= pyqtSignal(str)
	onfinish		= pyqtSignal(int, int, str)

	def __init__(self, parent, encoding = None):
		super(Process, self).__init__(parent)
		self.setObjectName('process')
		self.started.connect(self.onstart)
		self.error.connect(self.errorHandler)
		self.finished.connect(self.finishedHandler)
		self.stateChanged.connect(self.stateChangedHandler)
		self.readyReadStandardOutput.connect(self.stdOutHandler)
		self.readyReadStandardError.connect(self.stdErrHandler)
		self.encoding = encoding

	# Methods

	def decode(self, bytes):
		if self.encoding:
			return str(bytes, self.encoding)
		try:
			return str(bytes, sys.getfilesystemencoding())
		except:
			pass
		try:
			return str(bytes, sys.getdefaultencoding())
		except:
			pass
		return str(bytes)[2:-1]

	# Slots

	# 启动进程
	@pyqtSlot(str)
	def start(self, command):
		if self.state() == 0:
			super(Process, self).start(command)

	# 等待进程开始
	@pyqtSlot(result = bool)
	@pyqtSlot(int, result = bool)
	def waitForStarted(self, msec = 30000):
		return super(Process, self).waitForStarted(msec)

	# 等待进程完成
	@pyqtSlot(result = bool)
	@pyqtSlot(int, result = bool)
	def waitForFinished(self, msec = 30000):
		return super(Process, self).waitForFinished(msec)

	# 设置输入文件
	@pyqtSlot(str)
	def setStdInFile(self, filename):
		self.setStandardInputFile(filename)

	# 设置输出文件
	@pyqtSlot(str)
	def setStdOutFile(self, filename):
		self.setStandardOutputFile(filename)

	# 设置错误输出文件
	@pyqtSlot(str)
	def setStdErrFile(self, filename):
		self.setStandardErrorFile(filename)

	# 设置输出进程
	@pyqtSlot(QObject)
	def setStdOutProcess(self, process):
		self.setStandardOutputProcess(process)

	# 写入信息
	@pyqtSlot(str)
	def send(self, data):
		self.write(data)

	# 获取状态码
	@pyqtSlot(result = int)
	def state(self):
		return super(Process, self).state()

	# 获取状态信息
	@pyqtSlot(result = str)
	def stateStr(self):
		return Process.ProcessState[self.state()]

	# 获取错误码
	@pyqtSlot(result = int)
	def errno(self):
		return self.error()

	# 获取错误信息
	@pyqtSlot(result = str)
	def errorStr(self):
		return Process.ProcessError[self.error()]

	# 获取退出码
	@pyqtSlot(result = int)
	def exitCode(self):
		return super(Process, self).exitCode()

	# 获取退出状态码
	@pyqtSlot(result = int)
	def exitStatus(self):
		return super(Process, self).exitStatus()

	# 获取退出状态信息
	@pyqtSlot(result = str)
	def exitStatusStr(self):
		return Process.ExitStatus[self.exitStatus()]

	# 获取进程名
	@pyqtSlot(result = str)
	def program(self):
		return super(Process, self).program()

	# 获取参数列表
	@pyqtSlot(result = str)
	def argumentList(self):
		return '\n'.join(super(Process, self).arguments())

	# 获取参数
	@pyqtSlot(result = str)
	def arguments(self):
		return '"' + '" "'.join(super(Process, self).arguments()) + '"'

	# 设置工作目录
	@pyqtSlot(str)
	def setWorkingDirectory(self, directory):
		super(Process, self).setWorkingDirectory(directory)

	# 获取工作目录
	@pyqtSlot(result = str)
	def workingDirectory(self):
		return super(Process, self).workingDirectory()

	# 获取环境变量
	@pyqtSlot(result = str)
	def systemEnvironment(self):
		return self.systemEnvironment()

	# Sinals

	def errorHandler(self, error):
		self.onerror.emit(error, Process.ProcessError[error])

	def stdOutHandler(self):
		self.onstdout.emit(self.decode(self.readAllStandardOutput()))

	def stdErrHandler(self):
		self.onstderr.emit(self.decode(self.readAllStandardError()))

	def stateChangedHandler(self, state):
		self.onstatechange.emit(state, Process.ProcessState[state])

	def finishedHandler(self, exitCode, exitStatus):
		self.onfinish.emit(exitCode, exitStatus, Process.ExitStatus[exitStatus])
