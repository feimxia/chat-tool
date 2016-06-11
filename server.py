#coding:utf-8

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from server_ui import Ui_Form
import string,codecs
import sys
import socket
import time
from threading import *

reload(sys) 
sys.setdefaultencoding('utf8')

class MyForm(QtGui.QMainWindow,Ui_Form):
	
	
	def __init__(self,parent=None):
		super(MyForm,self).__init__(parent)
		self.setupUi(self)
		
		self.th = startThread()
		
		self.connect(self.pushButton_2,SIGNAL("clicked()"),self.get_ipandport)
		QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed"), self.receiveMessage)
		QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"), self.sendMessage)
		QtCore.QObject.connect(self.th, QtCore.SIGNAL("newget"), self.newget)
		
	def newget(self,address):
		theTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
		ch_message=str(address)
		message = theTime+"  "+ch_message+u"连接成功"+"!!!"+'\n'
		self.textBrowser.append(message)
		
	def get_ipandport(self):
		ip=str(self.lineEdit.text())
		port=int(self.lineEdit_2.text())
		self.pushButton_2.setEnabled(False)
		self.th.createsocket(ip,port)
		self.th.start()
		
	def receiveMessage(self,address): 
		self.textBrowser.append((str(address)).decode('utf-8'))
		self.textBrowser.append((self.th.message).decode('utf-8'))
		
	def sendMessage(self):
		#得到用户输入的消息
		message = self.textEdit.toPlainText()
		self.textEdit.clear()
		ch_message = str(message).decode('utf-8')
		#格式化当前的时间
		theTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
		name = '服务器 ~.~   '.decode('utf-8')
		header = name+theTime+'\n'
		message = header+ch_message+'\n'
		self.textBrowser.append(message)
		self.th.th_sendMessage(message)

class startThread(QtCore.QThread):
	def __init__(self):
		super(startThread,self).__init__() 
		self.message = ''
		self.cnume=[]
		self.falg=False
		
	def createsocket(self,ip,port):
		#self.host = '127.0.0.1'#按局域网情况修改
		#self.port = 8067
		self.host=ip
		self.port=port
		#建立socket连接
		self.severSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.severSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

		#socket绑定该主机的ip和端口
		self.severSocket.bind((self.host,self.port))
		self.severSocket.listen(15)
		self.buffer = 1024
		self.severSocket.listen(15)

	def run(self):
		while True:
			try:
				connection,address = self.severSocket.accept()
				self.cnume.append(connection)
				self.emit(SIGNAL("newget"),address)
				self.t1=Thread(target=self.recvthread,args=[connection,address])
				self.t1.start()
				print self.cnume
			except:
				continue
		
	def recvthread(self,connection,address):
		while True:
			msg = connection.recv(self.buffer)
			if msg != '':
				self.message = msg
				self.emit(SIGNAL("pressed"),address)
			else:
				self.message = self.message
		connection.close()
	
	def th_sendMessage(self,textMessage):
		for i in self.cnume:
			try:
				i.send(textMessage)
			except socket.error:
				raise

if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	myapp=MyForm()
	myapp.show()
	sys.exit(app.exec_())
