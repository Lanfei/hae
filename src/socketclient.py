import socket
from threading import Lock, Thread
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

class SocketClient(QObject, Thread):

	onopen = pyqtSignal()
	onmessage = pyqtSignal(str)
	onclose = pyqtSignal()
	onerror = pyqtSignal(int, str)

	def __init__(self, parent, encoding = 'utf-8'):
		super(SocketClient, self).__init__(parent)
		self.setObjectName('socketClient')
		self.setDaemon(True)
		self.encoding = encoding
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
			self.onclose.emit()
		except:
			pass

	# Slots

	# 连接Socket服务端
	@pyqtSlot(str, int, result = bool)
	def connect(self, host, port):
		try:
			self.conn.connect((host, port))
			self.onopen.emit()
			self.start()
			return True
		except Exception as e:
			self.onerror.emit(e.errno, e.strerror)
		return False

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
