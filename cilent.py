# -*- coding: utf-8 -*-
#Filename:Chat_Client.py
#基于Socket的局域网聊天客户端
 
from PyQt4 import QtCore,QtGui
from client_ui import Ui_Form
from PyQt4.QtCore import pyqtSignature
import socket
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
class ChatClient(QtGui.QMainWindow,Ui_Form):
    flag=False
    def __init__(self,parent=None):
        super(ChatClient,self).__init__(parent)
        self.setupUi(self)

        self.host = '127.0.0.1'#按局域网情况修改
        self.port = 8067
        #建立Socket连接
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientSocket.connect((self.host,self.port))
 
        self.th = startThread(self.clientSocket)
        self.th.start()
        QtCore.QObject.connect(self.th, QtCore.SIGNAL("pressed()"), self.receiveMessage)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"), self.sendMessage)
 
    #接收消息
    def receiveMessage(self):
        #接收服务器端信息
        self.textBrowser.append((self.th.message).decode('utf-8'))
 
    #发送消息
    def sendMessage(self):
        #得到用户输入的消息
        message = self.textEdit.toPlainText()
        self.textEdit.clear()
        ch_message = str(message).decode('utf-8')
        #格式化当前的时间
        theTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        name = '客户端 ~.~   '.decode('utf-8')
        header = name+theTime+'\n'
        message = header+ch_message+'\n'
        self.textBrowser.append(message)
        self.clientSocket.send(message)
 
class startThread(QtCore.QThread):
    pressed=QtCore.pyqtSignal()
    def __init__(self, s):
        super(startThread, self).__init__()
        self.s = s
        self.message=""
 
    def run(self):
        self.buffer = 1024
        while True:
            msg = self.s.recv(self.buffer)
            if msg !="":
                self.message=msg
                print msg
                self.pressed.emit()
            else:
                self.message=self.message
 
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())
