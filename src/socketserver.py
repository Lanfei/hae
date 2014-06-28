import socket
from threading import Lock, Thread
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

class SocketServer(QObject, Thread):

	onopen = pyqtSignal()
	onconnect = pyqtSignal(QObject)
	onmessage = pyqtSignal(QObject, str)
	ondisconnect = pyqtSignal(QObject)
	onclose = pyqtSignal()
	onerror = pyqtSignal(int, str)

	def __init__(self, parent, encoding = 'utf-8', timeout = None):
		super(SocketServer, self).__init__(parent)
		self.setObjectName('socketServer')
		self.setDaemon(True)
		self.encoding = encoding
		self.timeout = timeout
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def run(self):
		lock = Lock()
		while True:
			try:
				lock.acquire()
				conn, addr = self.socket.accept()
				socketConn = SocketConn(self, conn, self.encoding, self.timeout)
				self.onconnect.emit(socketConn)
				lock.release()
			except Exception as e:
				print(e)
				break
		try:
			self.onclose.emit()
		except:
			pass

	# Slots

	# 监听端口
	@pyqtSlot(int, result = bool)
	def listen(self, port):
		try:
			self.socket.bind(('', port))
			self.socket.listen(10)
			self.start()
			self.onopen.emit()
			return True
		except Exception as e:
			self.onerror.emit(e.errno, e.strerror)
		return False

	# 停止监听
	@pyqtSlot()
	def close(self):
		self.socket.close()

	# Sinals

	def messageHandler(self, socketConn, message):
		self.onmessage.emit(socketConn, message)

	def disconnectHandler(self, socketConn):
		self.ondisconnect.emit(socketConn)

class SocketConn(QObject, Thread):

	onmessage = pyqtSignal(str)
	onclose = pyqtSignal()
	onerror = pyqtSignal(int, str)

	def __init__(self, parent, conn, encoding = 'utf-8', timeout = None):
		super(SocketConn, self).__init__()
		self.setObjectName('socketConn')
		self.parent = parent
		self.conn = conn
		self.encoding = encoding
		self.conn.settimeout(timeout)
		self.setDaemon(True)
		self.start()

	# Methods

	def run(self):
		lock = Lock()
		while True:
			try:
				lock.acquire()
				bytes = self.conn.recv(1024)
				if bytes:
					self.messageHandler(bytes)
				else:
					break
				lock.release()
			except Exception as e:
				print(e)
				break
		try:
			self.close()
			self.onclose.emit()
			self.parent.disconnectHandler(self)
		except:
			pass

	# Slots

	# 发送数据
	@pyqtSlot(str, result = int)
	def send(self, message):
		try:
			bytes = bytearray(message, self.encoding)
			return self.conn.send(bytes)
		except:
			return 0

	# 关闭连接
	@pyqtSlot()
	def close(self):
		self.conn.close()

	# Sinals

	def messageHandler(self, bytes):
		message = str(bytes, self.encoding)
		self.onmessage.emit(message)
		self.parent.messageHandler(self, message)
