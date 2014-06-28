import assets
from PyQt5.Qt import QSettings
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar

class DataJar(QNetworkCookieJar):
	def __init__(self):
		super(DataJar, self).__init__()
		self.settings = QSettings(assets.fs.dataPath() + '/data.ini', QSettings.IniFormat)
		self.load()

	def load(self):
		strCookies = self.settings.value('cookies')
		if strCookies:
			self.setAllCookies(QNetworkCookie.parseCookies(strCookies))

	def save(self):
		cookies = self.allCookies()
		strCookies = ''
		for cookie in cookies:
			strCookies += cookie.toRawForm() + '\n'
		self.settings.setValue('cookies', strCookies)

	def set(self, name, value):
		self.settings.setValue('Data/' + name, value)

	def get(self, name):
		return self.settings.value('Data/' + name)

	def remove(self, name = None):
		if name is None:
			self.settings.remove('Data')
		else:
			self.settings.remove('Data/' + name)
