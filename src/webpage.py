import assets
import webbrowser
from PyQt5.Qt import QMessageBox
from PyQt5.QtNetwork import QNetworkDiskCache
from PyQt5.QtWebKitWidgets import QWebPage, QWebInspector

class WebPage(QWebPage):
	def __init__(self):
		super(WebPage, self).__init__()
		self.inspector = QWebInspector()
		self.inspector.setPage(self)
		self.inspector.resize(1024, 400)
		diskCache = QNetworkDiskCache(self)
		diskCache.setCacheDirectory(assets.fs.dataPath() + '/Cache')
		self.networkAccessManager().setCache(diskCache)
		self.networkAccessManager().setCookieJar(assets.dataJar)

	def acceptNavigationRequest(self, frame, request, type):
		if(type == QWebPage.NavigationTypeLinkClicked):
			url = request.url().toString()
			if(frame == self.mainFrame()):
				self.view().load(url)
				return False
			elif frame == None:
				# self.createWindow(QWebPage.WebBrowserWindow, url)
				webbrowser.open(request.url().toString())
				return False
		return QWebPage.acceptNavigationRequest(self, frame, request, type)

	# def downloadRequested(self, request):
	# 	print(request)

	def findText(self, text):
		return super(WebPage, self).findText(text, QWebPage.FindBackward)

	def showInspector(self):
		self.inspector.show()
		self.inspector.activateWindow()

	def hideInspector(self):
		self.inspector.close()

	def createWindow(self, type, url = None):
		from window import Window
		window = Window(self.view().parentWidget(), url, isDialog = (type == QWebPage.WebModalDialog))
		return window.webView.page()

	def javaScriptAlert(self, frame, msg):
		QMessageBox.information(self.view().parentWidget(), None, msg)

	def javaScriptConfirm(self, frame, msg):
		return QMessageBox.question(self.view().parentWidget(), None, msg) == QMessageBox.Yes

	# There is a bug in PyQt
	# def javaScriptPrompt(self, frame, msg, defaultValue):
	# 	result = QInputDialog.getText(self.view().parentWidget(), None, msg)
	# 	return (result[1], result[0])

	def close(self):
		self.hideInspector()
		assets.dataJar.save()
