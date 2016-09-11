import sys

from PyQt4 import QtGui, QtCore
from Copier import Copier

class DragDropDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(DragDropDialog, self).__init__()
        self.messageBrowser = QtGui.QTextBrowser(self)
        self.messageBrowser.setGeometry(QtCore.QRect(0, 0, 580, 380))
        self.copier = Copier()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(DragDropDialog, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(DragDropDialog, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():                
                messages = self.copier.copy(str(url.toLocalFile()))
                for message in messages:
                    self.messageBrowser.append(message)

            event.acceptProposedAction()
        else:
            super(DragDropDialog,self).dropEvent(event)

class MyWindow(QtGui.QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setGeometry(100,100,600,400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("FlexCopier")

        self.dialog = DragDropDialog(self)
        self.dialog.setGeometry(QtCore.QRect(0, 0, 600, 400))
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.dialog)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
