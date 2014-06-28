import os
import re
import json
import assets
from webpage import WebPage
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.Qt import Qt, QWebSettings, QPainter, QImage, QMimeData, QDrag, QUrl

class WebView(QWebView):
	def __init__(self, parent, url = ''):
		super(WebView, self).__init__(parent)
		self.draging = False
		self.drag = QDrag(self)
		self.webPage = WebPage()
		self.setPage(self.webPage)
		self.mainFrame = self.page().mainFrame()
		self.setAttribute(Qt.WA_DeleteOnClose, True)
		self.titleChanged.connect(parent.setWindowTitle)
		self.load(url)
		webSettings = self.settings()
		webSettings.setDefaultTextEncoding("utf-8")
		# webSettings.setOfflineStorageDefaultQuota(sys.maxsize)
		# webSettings.setOfflineWebApplicationCacheQuota(sys.maxsize)
		webSettings.enablePersistentStorage(assets.fs.dataPath())
		webSettings.setAttribute(QWebSettings.PluginsEnabled, True)
		webSettings.setAttribute(QWebSettings.DnsPrefetchEnabled, True)
		webSettings.setAttribute(QWebSettings.XSSAuditingEnabled, True)
		webSettings.setAttribute(QWebSettings.CSSGridLayoutEnabled, True)
		webSettings.setAttribute(QWebSettings.ScrollAnimatorEnabled, True)
		webSettings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
		webSettings.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
		webSettings.setAttribute(QWebSettings.JavascriptCanCloseWindows, True)
		webSettings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, True)
		webSettings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
		webSettings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
		self.mainFrame.javaScriptWindowObjectCleared.connect(self.setJavaScriptObject)
		self.mainFrame.iconChanged.connect(self.changeIcon)

	def load(self, url = ''):
		p = re.compile('(^file:\/\/)|(^http:\/\/)|(^https:\/\/)|(^data:)')
		if url and p.match(url) == None:
			url = QUrl.fromLocalFile(os.path.abspath(url))
		else:
			url = QUrl(url)
		super(WebView, self).load(url)

	def eval(self, javaScript):
		return self.mainFrame.evaluateJavaScript(javaScript)

	def changeIcon(self):
		self.parentWidget().setWindowIcon(self.mainFrame.icon())
		# self.parentWidget().setWindowIcon(QWebSettings.iconForUrl(self.url()))

	def setJavaScriptObject(self):
		self.mainFrame.addToJavaScriptWindowObject('HAE', self.parentWidget().api)
		self.mainFrame.addToJavaScriptWindowObject('HAE_app', self.parentWidget())
		self.mainFrame.addToJavaScriptWindowObject('HAE_fs', assets.fs)
		self.mainFrame.addToJavaScriptWindowObject('HAE_sys', assets.sys)
		self.mainFrame.addToJavaScriptWindowObject('HAE_codec', assets.codec)
		self.eval('''
			(function(){
				initModule('fs');
				initModule('sys');
				initModule('app');
				initModule('codec');
				initClass('Window');
				initClass('Dialog');
				initClass('FileDialog');
				initClass('File');
				initClass('Menu');
				initClass('MenuItem');
				initClass('TrayIcon');
				initClass('Downloader');
				initClass('Process');
				initClass('SocketServer');
				initClass('SocketClient');
				function initClass(name){
					HAE[name] = function(){
						return initEventBinder(HAE['create' + name].apply(window, arguments));
					};
				}
				function initModule(name){
					var key = 'HAE_' + name;
					HAE[name] = initEventBinder(window[key]);
					delete window[key];
				}
				function initEventBinder(object){
					object.addEvent = function(event, handler){
						if(typeof event == 'string'){
							var eventName = event;
							event = ('on' + event).toLowerCase();
							if(event in this && this[event].connect){
								this[event].connect(handler);
							}else{
								console.warn('Warning: This object dose not have "' + eventName + '" event');
							}
						}else if(typeof event == 'object'){
							for(var key in event){
								this.addEvent(key, event[key]);
							}
						}
					};
					object.removeEvent = function(event, handler){
						event = 'on' + event;
						console.log(this[event]);
						if(event in this && this[event].connect){
							this[event].disconnect(handler);
						}
					};
					return object;
				}
			})();
		''')

	def mousePressEvent(self, event):
		self.parentWidget().mousePressEvent(event)
		if not self.parentWidget().isDraging():
			super(WebView, self).mousePressEvent(event)
			if event.buttons() == Qt.LeftButton:
				mimeData = QMimeData()
				hitTestResult = self.mainFrame.hitTestContent(event.pos())
				# print(hitTestResult.linkUrl())
				# dragging the scrollbar
				if hitTestResult.isNull():
					self.draging = True
				if hitTestResult.isContentSelected():
					mimeData.setText(self.selectedText())
					mimeData.setHtml(self.selectedHtml())
				elif not hitTestResult.linkUrl().isEmpty():
					mimeData.setUrls([hitTestResult.linkUrl()])
					mimeData.setHtml(hitTestResult.element().toOuterXml())
				elif not hitTestResult.pixmap().isNull():
					mimeData.setImageData(hitTestResult.pixmap())
					mimeData.setUrls([hitTestResult.imageUrl()])
					mimeData.setHtml(hitTestResult.element().toOuterXml())
					# mimeData.setData('application/x-qt-windows-mime;value="FileContents"', QVariant(hitTestResult.pixmap()).toByteArray())
				# elif not hitTestResult.mediaUrl().isEmpty():
				# 	mimeData.setUrls([hitTestResult.mediaUrl()])
				# 	mimeData.setHtml(hitTestResult.element().toOuterXml())
				else:
					return
				# pixmap = hitTestResult.pixmap()
				# pixmap.setMask(QBitmap.fromImage(pixmap.toImage()))
				self.drag.setMimeData(mimeData)
				# self.drag.setPixmap(pixmap)
				# self.drag.setHotSpot(QPoint(self.drag.pixmap().width() / 2, self.drag.pixmap().height() / 2))

	def mouseMoveEvent(self, event):
		if not self.parentWidget().isDraging():
			super(WebView, self).mouseMoveEvent(event)
			if self.drag.mimeData():
				self.drag.exec()
				self.drag.setMimeData(None)
		if not self.draging:
			event.ignore()

	def mouseReleaseEvent(self, event):
		self.draging = False
		super(WebView, self).mouseReleaseEvent(event)
		self.drag.setMimeData(None)
		event.ignore()

	def close(self):
		self.stop()
		self.load()
		self.page().close()
		self.eval('HAE = null')
		self.drag.setMimeData(None)
		super(WebView, self).close()
