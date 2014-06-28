import base64
import hashlib
from PyQt5.QtCore import QObject, pyqtSlot

class Codec(QObject):

	# Base64编码
	@pyqtSlot(str, result = str)
	def base64Encode(self, data):
		return str(base64.b64encode(data.encode()), 'utf-8')

	# Base64解码
	@pyqtSlot(str, result = str)
	def base64Decode(self, data):
		return str(base64.b64decode(data.encode()), 'utf-8')

	# md5编码
	@pyqtSlot(str, result = str)
	def md5(self, data):
		return hashlib.md5(data.encode()).hexdigest()

	# sha1编码
	@pyqtSlot(str, result = str)
	def sha1(self, data):
		return hashlib.sha1(data.encode()).hexdigest()

	# sha224编码
	@pyqtSlot(str, result = str)
	def sha224(self, data):
		return hashlib.sha224(data.encode()).hexdigest()

	# sha256编码
	@pyqtSlot(str, result = str)
	def sha256(self, data):
		return hashlib.sha256(data.encode()).hexdigest()

	# sha384编码
	@pyqtSlot(str, result = str)
	def sha384(self, data):
		return hashlib.sha384(data.encode()).hexdigest()

	# sha512编码
	@pyqtSlot(str, result = str)
	def sha512(self, data):
		return hashlib.sha512(data.encode()).hexdigest()
