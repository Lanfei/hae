import os
import tempfile
from urllib.error import *
from urllib.request import *
from threading import Lock, Thread
from PyQt5.Qt import QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal

class Downloader(QObject, Thread):

	onstart = pyqtSignal()
	onprogress = pyqtSignal(int, int)
	onfinish = pyqtSignal(int)
	onerror = pyqtSignal(int, str)

	def __init__(self, parent, url, filename = None, resume = False):
		super(Downloader, self).__init__(parent)
		self.setObjectName('downloader')
		self.url = url
		self.file = None
		self.filename = filename
		if not resume:
			self.cancel()
		self.setDaemon(True)
		# self.start()

	def run(self):
		try:
			size = -1
			read = self.size()

			request = Request(self.url)
			if read > 0:
				request.add_header('range', 'bytes=' + str(read) + '-')
			response = urlopen(request)
			headers = response.info()

			if read > 0 and 'Content-Range' in headers:
				ranges = headers['Content-Range']
				size = int(ranges.split('/')[-1].strip())
				self.open('ab')
			else:
				if 'Content-Length' in headers:
					size = int(headers['Content-Length'])
				self.open('wb')

			with self.file:
				bs = 1024 * 8
				lock = Lock()
				self.onstart.emit()
				while True:
					lock.acquire()
					block = response.read(bs)
					if not block or self.file.closed:
						break
					read += len(block)
					self.file.write(block)
					self.onprogress.emit(read, size)
					lock.release()
				self.file.close()
				self.onfinish.emit(read)

		except HTTPError as error:
			self.onerror.emit(error.code, error.msg)
		except URLError as error:
			self.onerror.emit(error.reason.errno, error.reason.strerror)
		except Exception as error:
			self.onerror.emit(-1, str(error))

	def open(self, mode):
		if self.filename:
			self.file = open(self.filename, mode)
		else:
			self.file = tempfile.NamedTemporaryFile()
			self.filename = self.file.name

	def size(self):
		try:
			return os.path.getsize(self.filename)
		except:
			return 0

	# 获取文件路径
	@pyqtSlot(result = str)
	def getFilename(self):
		return self.filename

	# 开始下载任务
	@pyqtSlot()
	def start(self):
		super(Downloader, self).start()

	# 停止下载任务
	@pyqtSlot()
	def stop(self):
		if self.file:
			self.file.close()

	# 取消下载任务
	@pyqtSlot()
	def cancel(self):
		self.stop()
		if self.filename and os.path.exists(self.filename):
			os.unlink(self.filename)
