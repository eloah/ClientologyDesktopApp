#Desktop app for client base with personal cards for each client.
#Utilizes PySide library for GUI development
#Utilizes sqlite3 for Database

import sys
import smtplib
from sqlite3 import *
from PySide.QtGui import *
from PySide.QtCore import *

qu = 0

#Open client window class
class openClient(QWidget):
    findSend = Signal(str)
    removeSend = Signal(str)
    def __init__(self, parent = None):
        super(openClient, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Client search")
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 180)
        self.setMaximumSize(500, 180)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.combo = QComboBox(self)
        self.combo.setCurrentIndex(0)
        self.combo.setGeometry(100, 35, 300, 40)
        self.combo.setCursor(Qt.PointingHandCursor)
        self.combo.setStyleSheet("QComboBox{font-size:20px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-radius:20px;}"
                                 "QComboBox::drop-down{subcontrol-origin: padding; subcontrol-position: right; border-left-color: darkgray; width: 50px;border-left-width: 2px;border-left-style: solid; border-left-color:#006666;}"
                                 "QComboBox::down-arrow{image:url(Icons/dott.png);}"
                                 "QComboBox QAbstractItemView {selection-background-color: teal; background-color:white;}")
        
        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(100, 100, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}" 
                                 "QPushButton:hover{image: url('Icons/okhov.png');}")

        self.removeBtn = QPushButton("", self)
        self.removeBtn.setGeometry(225, 100, 50, 50)
        self.removeBtn.setCursor(Qt.PointingHandCursor)
        self.removeBtn.setStyleSheet("QPushButton{image: url('Icons/remuser.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/remuserhov.png');}")

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(355, 100, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.warningWindow = warningWindow()

        self.okBtn.clicked.connect(self.findCl)
        self.removeBtn.clicked.connect(self.removeCl)
        self.cancelBtn.clicked.connect(self.close)
        
    def chooseClient(self):
        self.combo.clear()
        self.combo.addItem("Choose a client")
        conn = connect("Data/Database.db", detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        c.execute('SELECT cNAME FROM CUSTOMER')
        idc = c.fetchall()

        for i in enumerate(idc):
            add = str(idc[i[0]][0])
            self.combo.addItem(add)

        conn.commit()
        conn.close()

    def findCl(self):
        find = self.combo.currentText()
        if self.combo.currentText() == "Choose a client":
            status = 4
            self.warningWindow.openWarningWindow(status)
        else:
            self.findSend.emit(find)
            self.close()

    def removeCl(self):
        remove = self.combo.currentText()
        if self.combo.currentText() == "Choose a client":
            status = 4
            self.warningWindow.openWarningWindow(status)
        else:
            self.removeSend.emit(remove)



class updateClient(QWidget):
    saveSend = Signal(int)
    def __init__(self, parent = None):
        super(updateClient, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Save new info")
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 180)
        self.setMaximumSize(500, 180)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("    Do you want to save new info or PDF?    ", self)
        self.label.setGeometry(50, 30, 415, 50) 
        self.label.setStyleSheet("font-size:20px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.saveBtn = QPushButton("", self)
        self.saveBtn.setGeometry(100, 100, 50, 50)
        self.saveBtn.setCursor(Qt.PointingHandCursor)
        self.saveBtn.setStyleSheet("QPushButton{image: url('Icons/save.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/savehov.png');}")

        self.pdfBtn = QPushButton("", self)
        self.pdfBtn.setGeometry(225, 100, 50, 50)
        self.pdfBtn.setCursor(Qt.PointingHandCursor)
        self.pdfBtn.setStyleSheet("QPushButton{image: url('Icons/savepdf.png'); background:transparent;}" 
                                  "QPushButton:hover{image: url('Icons/savepdfhov.png');}")

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(355, 100, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.saveBtn.clicked.connect(self.saveTable)
        self.pdfBtn.clicked.connect(self.savePdf)
        self.cancelBtn.clicked.connect(self.close)

    def saveTable(self):
        save = 1
        self.saveSend.emit(save)
        self.close()

    def savePdf(self):
        save = 2
        self.saveSend.emit(save)
        self.close()

#Closing app window class
class closeWindow(QWidget):
    closeSend = Signal(int)
    def __init__(self, parent = None):
        super(closeWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Shutdown")
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 180)
        self.setMaximumSize(500, 180)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("",self)
        self.label.setGeometry(50, 30, 410, 50)
        self.label.setStyleSheet("font-size:20px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(140, 100, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}" 
                                 "QPushButton:hover{image: url('Icons/okhov.png');}")

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(310, 100, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.okBtn.clicked.connect(self.closeW)
        self.okBtn.clicked.connect(self.close)
        self.cancelBtn.clicked.connect(self.close)

    def quit(self, close):
        global qu
        if close == 1:
            qu = 1
            self.label.setText("    Do you want to quit the app?    ")   
        elif close == 2:
            qu = 2
            self.label.setText("    Did you save all the changes?    ")
        self.show()

    def closeW(self):
        global qu
        if qu == 1:
            quit = 1
            self.closeSend.emit(quit)
        elif qu == 2:
            quit = 2
            self.closeSend.emit(quit)
        self.close()


#Adding new client to database window class 
class newClient(QWidget):
    send = Signal(str,str,str)
    def __init__(self, parent = None):
        super(newClient, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add a new client')
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 400)
        self.setMaximumSize(500, 400)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("Client info", self)
        self.label.setGeometry(50, 12, 410, 50)
        self.label.setStyleSheet("font-size:30px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.nameLbl = QLabel("Full name", self)
        self.nameLbl.setGeometry(50, 70, 100, 50)
        self.nameLbl.setStyleSheet("font-size:24px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.nameLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.afmLbl = QLabel("Reg", self)
        self.afmLbl.setGeometry(50, 150, 100, 50)
        self.afmLbl.setStyleSheet("font-size:24px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.afmLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.phoneLbl = QLabel("Tel", self)
        self.phoneLbl.setGeometry(50, 230, 100, 50)
        self.phoneLbl.setStyleSheet("font-size:24px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.phoneLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(140, 306, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}" 
                                 "QPushButton:hover{image: url('Icons/okhov.png');}")

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(310, 306, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.n = QLineEdit(self) 
        self.n.setGeometry(190, 76, 260, 40) 
        self.n.setStyleSheet('font-size:20px; font-family:Calibri; font-weight:bold; border:2px solid #006666; border-radius:20px;')    
        self.n.setAlignment(Qt.AlignCenter)

        self.a = QLineEdit(self)
        self.a.setGeometry(190, 156, 260, 40)
        self.a.setMaxLength(10)
        self.a.setStyleSheet('font-size:20px; font-family:Calibri; font-weight:bold; border:2px solid #006666; border-radius:20px;')
        self.a.setAlignment(Qt.AlignCenter)

        self.p = QLineEdit(self)
        self.p.setGeometry(190, 236, 260, 40)
        self.p.setMaxLength(10)
        self.p.setStyleSheet('font-size:20px; font-family:Calibri; font-weight:bold; border:2px solid #006666; border-radius:20px;')
        self.p.setAlignment(Qt.AlignCenter)

        self.warningWindow = warningWindow()

        self.okBtn.clicked.connect(self.addNewClient)
        self.cancelBtn.clicked.connect(self.close)


    def addNewClient(self):
        na = self.n.text()
        af = self.a.text()
        ph = self.p.text()
        if na and af and ph:
            try:
                int(af)
                int(ph)
                self.send.emit(na,af,ph)
                self.n.clear()
                self.a.clear()
                self.p.clear()
                self.close()
            except ValueError:
                status = 8
                self.warningWindow.openWarningWindow(status)
        else:
            status = 2
            self.warningWindow.openWarningWindow(status)


class newBill(QWidget):
    addSend = Signal(str)
    def __init__(self, parent = None):
        super(newBill, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Adding a new bill')
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 180)
        self.setMaximumSize(500, 180)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("Add a date of the bill", self)
        self.label.setGeometry(45, 15, 410, 20)
        self.label.setStyleSheet("font-size:20px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(140, 100, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}" 
                                 "QPushButton:hover{image: url('Icons/okhov.png');}")

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(310, 100, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.da = QLineEdit(self) 
        self.da.setGeometry(120, 50, 260, 40) 
        self.da.setStyleSheet('font-size:20px; font-family:Calibri; font-weight:bold; border:2px solid #006666; border-radius:20px;')    
        self.da.setAlignment(Qt.AlignCenter)

        self.warningWindow = warningWindow()

        self.okBtn.clicked.connect(self.addNewBill)
        self.cancelBtn.clicked.connect(self.close)


    def addNewBill(self):
        d = self.da.text()
        if d:
            self.addSend.emit(d)
            self.da.clear()
            self.close()
        else:
            status = 6
            self.warningWindow.openWarningWindow(status)

#Removing data from client card class
class removeBill(QWidget):
    remBl = Signal(str)
    def __init__(self, parent = None):
        super(removeBill, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Deleting a bill")
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 180)
        self.setMaximumSize(500, 180)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.combo = QComboBox(self)
        self.combo.setCurrentIndex(0)
        self.combo.setGeometry(100, 35, 300, 40)
        self.combo.setCursor(Qt.PointingHandCursor)
        self.combo.setStyleSheet("QComboBox{font-size:20px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-radius:20px;}"
                                 "QComboBox::drop-down{subcontrol-origin: padding; subcontrol-position: right; border-left-color: darkgray; width: 50px;border-left-width: 2px;border-left-style: solid; border-left-color:#006666;}"
                                 "QComboBox::down-arrow{image:url(Icons/dott.png);}"
                                 "QComboBox QAbstractItemView {selection-background-color: teal; background-color:white;}")
        
        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(100, 100, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}" 
                                 "QPushButton:hover{image: url('Icons/okhov.png');}")

        self.cancelBtn = QPushButton("", self)
        self.cancelBtn.setGeometry(355, 100, 50, 50)
        self.cancelBtn.setCursor(Qt.PointingHandCursor)
        self.cancelBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.warningWindow = warningWindow()

        self.okBtn.clicked.connect(self.removeBl)
        self.cancelBtn.clicked.connect(self.close)
        
    def chooseBill(self, bname):
        self.combo.clear()
        self.combo.addItem("Choose a date")
        conn = connect("Data/Database.db", detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        c.execute('SELECT DAT FROM BILL WHERE bNAME=? ORDER BY DAT',(bname,))
        idc = c.fetchall()

        list = []
        for i in enumerate(idc):
            seen = set(list)
            add = str(idc[i[0]][0])
            if add not in seen:
                list.append(add)
        self.combo.addItems(list)

        conn.commit()
        conn.close()

    def removeBl(self):
        remove = self.combo.currentText()
        if self.combo.currentText() == "Choose a date":
            status = 9
            self.warningWindow.openWarningWindow(status)
        else:
            self.remBl.emit(remove)
          
#Warning window class
class warningWindow(QWidget):
    
    def __init__(self, parent = None):
        super(warningWindow, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Warning!')
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(500, 180)
        self.setMaximumSize(500, 180)
        self.setStyleSheet("QWidget{background-color: white;}")
        self.label = QLabel("", self)
        self.label.setGeometry(32, 30, 430, 50)
        self.label.setStyleSheet("font-size:20px; font-family:Calibri; color:#006666; font-weight:bold;")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.okBtn = QPushButton("", self)
        self.okBtn.setGeometry(225, 100, 50, 50)
        self.okBtn.setCursor(Qt.PointingHandCursor)
        self.okBtn.setStyleSheet("QPushButton{image: url('Icons/ok.png'); background:transparent;}" 
                                 "QPushButton:hover{image: url('Icons/okhov.png');}")

        self.okBtn.clicked.connect(self.close)

    def openWarningWindow(self, status):
        if status == 1:
            self.label.setText("Columns 'DEBIT', 'CREDIT' και 'REMAIN' \ncan be only numbers!")
        elif status == 2:
            self.label.setText("    Please, add the whole info!    ")
        elif status == 3:
            self.label.setText("    Client not found! Please, try again    ")
        elif status == 4:
            self.label.setText("    Please, choose a client!   ")
        elif status == 5:
            self.label.setText("Columns 'LENGTH', 'HEIGT', 'S.M.', 'QTY.', \n'PRICE' and 'AMOUNT' can be only numbers!' ")
        elif status == 6:
            self.label.setText("    Please, add a date!    ")
        elif status == 7:
            self.label.setText("    There is no info for saving!    ")
        elif status == 8:
            self.label.setText("    Reg and Phone can be only numbers!")
        elif status == 9:
            self.label.setText("    Please, choose a date!    ")
        self.show()

#-------------------------------------------------------------------------------------------------
#Bill Window class

class billForm(QWidget):
    
    def __init__(self, parent = None):
        super(billForm, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Glass Expert - Orders')
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(930, 620)
        self.setMaximumSize(930, 620)
        self.setStyleSheet("QWidget{background-color: white;}" 
                           "QTableWidget{gridline-color:#006666; border:2px solid #006666; font-size:22px; font-family:Calibri;}"
                           "QHeaderView::section{font-size:18px; border-style:none; border-right:2px solid #006666;  color:#006666;}"
                           "QHeaderView::section:horizontal{padding:15px;font-size:18px; border-bottom:2px solid #006666;}"
                           "QHeaderView::section:vertical{font-size:12px; padding:6px; border-bottom:2px solid #006666;}")
        
        self.table = QTableWidget(self)
        self.table.setRowCount(1)
        self.table.setColumnCount(7)
        self.table.setGeometry(100, 100, 800, 455)
        self.colLabels = ["TYPE","LENGTH","HEIGHT","S.M.","QTY.","PRICE","AMOUNT"]
        self.table.setHorizontalHeaderLabels(self.colLabels)
        self.horizHeader = self.table.horizontalHeader()
        self.horizHeader.setResizeMode(0, QHeaderView.Stretch)
        self.horizHeader.setResizeMode(1, QHeaderView.Stretch)
        self.vertHeader = self.table.verticalHeader()
        self.vertHeader.setDefaultSectionSize(40)
        
        self.title = QLabel(self)
        self.title.setText("Glass Expert - Orders")
        self.title.setGeometry(150, 10, 600, 40)
        self.title.setStyleSheet("font-size:28px; font-family:Calibri; font-weight:bold; color:#006666;")
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        self.name = QLabel(self)
        self.name.setText("")
        self.name.setGeometry(100, 62, 408, 40)
        self.name.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-top-left-radius:20px;")
        self.name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.afm = QLabel(self)
        self.afm.setText("")
        self.afm.setGeometry(506, 62, 198, 40)
        self.afm.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666;")
        self.afm.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.phone = QLabel(self)
        self.phone.setText("")
        self.phone.setGeometry(702, 62, 198, 40)
        self.phone.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666;border-top-right-radius:20px;")
        self.phone.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.total = QLabel(self)
        self.total.setText("ΣΥΝΟΛΟ")
        self.total.setGeometry(702, 553, 100, 40)
        self.total.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-bottom-left-radius:20px;")
        self.total.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        self.price = QLabel(self)
        self.price.setText("0.00")
        self.price.setGeometry(800, 553, 100, 40)
        self.price.setStyleSheet("font-size:24px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-bottom-right-radius:20px; ")
        self.price.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.combo = QComboBox(self)
        self.combo.setCurrentIndex(0)
        self.combo.setGeometry(100, 553, 300, 40)
        self.combo.setStyleSheet("QComboBox{font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-bottom-left-radius:20px; border-bottom-right-radius:20px;}"
                                 "QComboBox::drop-down{subcontrol-origin: padding; subcontrol-position: right; border-left-color: darkgray; width: 50px;border-left-width: 2px;border-left-style: solid; border-left-color:#006666;}"
                                 "QComboBox::down-arrow{image:url(Icons/dott.png);}"
                                 "QComboBox QAbstractItemView {selection-background-color: teal; background-color:transparent;}")
        
        self.combo.setCurrentIndex(0)
        self.combo.setCursor(Qt.PointingHandCursor)
        
        self.addBtn = QPushButton(self)
        self.addBtn.setGeometry(25, 100, 50, 50)
        self.addBtn.setCursor(Qt.PointingHandCursor)
        self.addBtn.setStyleSheet("QPushButton{image: url('Icons/add.png'); background:transparent;}" 
                                  "QPushButton:hover{image: url('Icons/addhov.png');}")        

        self.copyBtn = QPushButton(self)
        self.copyBtn.setGeometry(25, 168, 50, 50)
        self.copyBtn.setCursor(Qt.PointingHandCursor)
        self.copyBtn.setStyleSheet("QPushButton{image: url('Icons/copy.png'); background:transparent;}" 
                                    "QPushButton:hover{image: url('Icons/copyhov.png');}")

        self.removeBtn = QPushButton(self)
        self.removeBtn.setGeometry(25, 236, 50, 50)
        self.removeBtn.setCursor(Qt.PointingHandCursor)
        self.removeBtn.setStyleSheet("QPushButton{image: url('Icons/remove.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/removehov.png');}")
        
        self.saveBtn = QPushButton(self)
        self.saveBtn.setGeometry(25, 302, 50, 50)
        self.saveBtn.setCursor(Qt.PointingHandCursor)
        self.saveBtn.setStyleSheet("QPushButton{image: url('Icons/save.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/savehov.png');}")
    
        self.addBillBtn = QPushButton(self)
        self.addBillBtn.setGeometry(25, 370, 50, 50)
        self.addBillBtn.setCursor(Qt.PointingHandCursor)
        self.addBillBtn.setStyleSheet("QPushButton{image: url('Icons/addbill.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/addbillhov.png');}")

        self.removeBillBtn = QPushButton(self)
        self.removeBillBtn.setGeometry(25, 438, 50, 50)
        self.removeBillBtn.setCursor(Qt.PointingHandCursor)
        self.removeBillBtn.setStyleSheet("QPushButton{image: url('Icons/rembill.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/rembillhov.png');}")
    
        self.quitBtn = QPushButton(self)
        self.quitBtn.setGeometry(25, 506, 50, 50)
        self.quitBtn.setCursor(Qt.PointingHandCursor)
        self.quitBtn.setStyleSheet("QPushButton{image: url('Icons/cancel.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/cancelhov.png');}")

        self.warningWindow = warningWindow()
        self.closeWindow = closeWindow()
        self.openCl = openClient()
        self.updateCl = updateClient()
        self.newBill = newBill()
        self.remBill = removeBill()

        self.addBtn.clicked.connect(self.addRow)
        self.copyBtn.clicked.connect(self.copyRow)
        self.removeBtn.clicked.connect(self.removeRow)
        self.saveBtn.clicked.connect(self.updateTable)
        self.addBillBtn.clicked.connect(self.addBill)
        self.removeBillBtn.clicked.connect(self.deleteBill)
        self.quitBtn.clicked.connect(self.quit)
        self.table.itemSelectionChanged.connect(self.addData)

        self.combo.currentIndexChanged.connect(self.dateChange)

        self.closeWindow.closeSend.connect(self.quitApp)
        self.newBill.addSend.connect(self.addNewBill)
        self.updateCl.saveSend.connect(self.saveTable)
        self.remBill.remBl.connect(self.remoBill)


    def addData(self):
        total = 0
        
        row = self.table.currentRow()
        column = self.table.currentColumn()
        rows = self.table.rowCount()

        if self.table.item(row, 1) and self.table.item(row, 2) and column == 3:
            width = self.table.item(row, 1).text()
            height = self.table.item(row, 2).text()
            try:
                float(width)
                float(height)
                tm = float(width)*float(height)
                tm = str('%.3f' % tm)
                self.table.setItem(row, 3, QTableWidgetItem(tm))
            except ValueError:
                status = 5
                self.warningWindow.openWarningWindow(status)
                
        if self.table.item(row,3) and self.table.item(row, 4) and self.table.item(row, 5)and column == 6:
            
            tm =  self.table.item(row, 3).text()  
            parts = self.table.item(row, 4).text()
            price = self.table.item(row, 5).text()
            
            try:
                int(parts)
                suma = float(tm)*int(parts)*float(price)
                suma = str('%.2f' % suma)
                self.table.setItem(row, 6, QTableWidgetItem(suma))
            except ValueError:
                status = 5
                self.warningWindow.openWarningWindow(status)
        
        for i in range(0, rows):
            if self.table.item(i, 6):
                item = self.table.item(i, 6).text()
                total += float(item)
                #print(total)
        tot = str('%.2f' % total)
        self.price.setText(tot)
        total = 0                  

    def addRow(self):
        currentRow = self.table.currentRow()
        self.table.insertRow(currentRow+1)

    def copyRow(self):
        row = self.table.currentRow()
        
        data = []
        for i in range(0,7):
            item = self.table.item(row, i)

            if item:
                item = self.table.item(row, i).text()
                data.append(item) 
            else:
                data.append('')
                  
        self.addRow()
        row += 1

        for i in range(0,7):
            itemCopy = data[i]
            self.table.setItem(row, i, QTableWidgetItem(itemCopy))

    def removeRow(self):
        currentRow = self.table.currentRow()
        self.table.removeRow(currentRow)

    def addBill(self):
        self.newBill.show()
        self.newBill.raise_()
        self.newBill.da.clear()

    def addNewBill(self, dat):
        self.combo.addItem(dat)

    def updateTable(self):
        self.updateCl.show()
        self.updateCl.raise_()

    def saveTable(self, save):
        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()
        dat = self.combo.currentText()
        bname = self.name.text()
        if save == 1 and dat!= "    Choose a date":
            c.execute('DELETE FROM BILL WHERE DAT=? AND bNAME=?',(dat,bname))

            lists = []
            for row in range(self.table.rowCount()):
                rowdata = []
                rowdata.append(self.name.text())
                rowdata.append(dat)
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')
                  
                    if len(rowdata) == 9:
                        lists.append(rowdata)
            print(lists)
            c.executemany('INSERT INTO BILL VALUES(?,?,?,?,?,?,?,?,?)', lists)

            c.execute('SELECT DAT FROM BILL WHERE bNAME=? ORDER BY DAT',(bname,))
            idc = c.fetchall()

            self.combo.clear()
            list = []
            for i in enumerate(idc):
                seen = set(list)
                add = str(idc[i[0]][0])
                if add not in seen:
                    list.append(add)
            self.combo.addItem("    Choose a date")
            self.combo.addItems(list)

            self.table.clearContents()

            if len(idc) == 0:
                self.table.setRowCount(0)
                self.table.insertRow(0)
            else:
                self.table.setRowCount(0)
                
            self.table.clearContents()

            info = c.execute('SELECT TYPE,WIDTH,HEIGHT,SQR,QUANTITY,PRICE,TOPAY FROM BILL WHERE DAT=? AND bNAME=? ORDER BY DAT',(dat,bname))    
            for row, rowdata in enumerate(info):
                self.table.insertRow(row)
                for column, data in enumerate(rowdata):
                    self.table.setItem(row, column , QTableWidgetItem(str(data)))

        elif save == 2 and dat!= "    Choose a date":
            pass

        else:
            status = 7
            self.warningWindow.openWarningWindow(status)

        conn.commit()
        conn.close()

    def deleteBill(self):
        self.bname = self.name.text()
        self.remBill.show()
        self.remBill.chooseBill(self.bname)

    def remoBill(self,rem):
        self.combo.clear()
        self.combo.addItem("    Choose a date")
        bname = self.name.text()
        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('DELETE FROM BILL WHERE DAT=? AND bNAME=?',(rem,bname))

        c.execute('SELECT DAT FROM BILL WHERE bNAME=? ORDER BY DAT',(self.bname,))
        idc = c.fetchall()

        list = []
        for i in enumerate(idc):
            seen = set(list)
            add = str(idc[i[0]][0])
            if add not in seen:
                list.append(add)
        self.combo.addItems(list)
        
        conn.commit()
        conn.close()

        self.remBill.chooseBill(self.bname)

    def dateChange(self):
        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        name = self.name.text()
        c.execute('SELECT DAT FROM BILL WHERE bNAME=? ORDER BY DAT',(name,))
        idc = c.fetchall()

        if len(idc) == 0:
            self.table.setRowCount(0)
            self.table.insertRow(0)
        else:
            self.table.setRowCount(0)
        ct = self.combo.currentText() 
        if ct == "    Choose a date":      
            self.table.clearContents()

        info = c.execute('SELECT TYPE,WIDTH,HEIGHT,SQR,QUANTITY,PRICE,TOPAY FROM BILL WHERE DAT=? AND bNAME=? ORDER BY DAT',(ct,name))  

        for row, rowdata in enumerate(info):
            self.table.insertRow(row)
            for column, data in enumerate(rowdata):
                self.table.setItem(row, column , QTableWidgetItem(str(data)))
        
        self.table.setHorizontalHeaderLabels(self.colLabels)                
        self.horizHeader.setResizeMode(1, QHeaderView.Stretch)
        self.horizHeader.setResizeMode(0, QHeaderView.Stretch)
            
        conn.commit()
        conn.close()

    def quit(self):
        close = 2
        self.closeWindow.quit(close)

    def quitApp(self, quit):
        if quit == 2:
            self.close()

#-------------------------------------------------------------------------------------------------
#Main Window class

class Client(QMainWindow):
    
    def __init__(self, parent = None):
        super(Client, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Glass Expert - Clientology')
        self.setWindowIcon(QIcon(QPixmap('Icons/main.png')))
        self.setMinimumSize(1000, 680)
        self.setMaximumSize(1000, 680)
        self.setStyleSheet("QMainWindow{background-color: white;}" 
                           "QTableWidget{gridline-color:#006666; border:2px solid #006666; font-size:22px; font-family:Calibri;}"
                           "QHeaderView::section{font-size:18px; border-style:none; border-right:2px solid #006666;  color:#006666;}"
                           "QHeaderView::section:horizontal{padding:15px;font-size:16px; font-weight:bold; border-bottom:2px solid #006666;}"
                           "QHeaderView::section:vertical{font-size:12px; padding:6px; border-bottom:2px solid #006666;}")
        
        self.table = QTableWidget(self.centralWidget)
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        self.table.setGeometry(150, 120, 800, 455)
        self.colLabels = ["DATE","INVOICE","DEBIT","CREDIT","REMAIN"]
        self.table.setHorizontalHeaderLabels(self.colLabels)
        self.horizHeader = self.table.horizontalHeader()
        self.horizHeader.setResizeMode(0, QHeaderView.Stretch)
        self.horizHeader.setResizeMode(1, QHeaderView.Stretch)

        self.vertHeader = self.table.verticalHeader()
        self.vertHeader.setDefaultSectionSize(40)
        
        self.title = QLabel(self.centralWidget)
        self.title.setText("Glass Expert - Clientology")
        self.title.setGeometry(200, 20, 600, 40)
        self.title.setStyleSheet("font-size:32px; font-family:Calibri; font-weight:bold; color:#006666;")
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.name = QLabel(self.centralWidget)
        self.name.setText("")
        self.name.setGeometry(150, 82, 408, 40)
        self.name.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-top-left-radius:20px;")
        self.name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.afm = QLabel(self.centralWidget)
        self.afm.setText("")
        self.afm.setGeometry(556, 82, 198, 40)
        self.afm.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666;")
        self.afm.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.phone = QLabel(self.centralWidget)
        self.phone.setText("")
        self.phone.setGeometry(752, 82, 198, 40)
        self.phone.setStyleSheet("font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666;border-top-right-radius:20px;")
        self.phone.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.total1 = QLabel(self.centralWidget)
        self.total1.setText("0.00")
        self.total1.setGeometry(654, 573, 100, 40)
        self.total1.setStyleSheet("font-size:24px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-bottom-left-radius:20px;")
        self.total1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.total2 = QLabel(self.centralWidget)
        self.total2.setText("0.00")
        self.total2.setGeometry(752, 573, 100, 40)
        self.total2.setStyleSheet("font-size:24px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666;")
        self.total2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.price = QLabel(self.centralWidget)
        self.price.setText("0.00")
        self.price.setGeometry(850, 573, 100, 40)
        self.price.setStyleSheet("font-size:24px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-bottom-right-radius:20px; ")
        self.price.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        self.addBtn = QPushButton(self.centralWidget)
        self.addBtn.setGeometry(50, 120, 50, 50)
        self.addBtn.setCursor(Qt.PointingHandCursor)
        self.addBtn.setStyleSheet("QPushButton{image: url('Icons/add.png'); background:transparent;}" 
                                  "QPushButton:hover{image: url('Icons/addhov.png');}")        

        self.copyBtn = QPushButton(self.centralWidget)
        self.copyBtn.setGeometry(50, 190, 50, 50)
        self.copyBtn.setCursor(Qt.PointingHandCursor)
        self.copyBtn.setStyleSheet("QPushButton{image: url('Icons/copy.png'); background:transparent;}" 
                                    "QPushButton:hover{image: url('Icons/copyhov.png');}")

        self.removeBtn = QPushButton(self.centralWidget)
        self.removeBtn.setGeometry(50, 260, 50, 50)
        self.removeBtn.setCursor(Qt.PointingHandCursor)
        self.removeBtn.setStyleSheet("QPushButton{image: url('Icons/remove.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/removehov.png');}")

        self.newBtn = QPushButton(self.centralWidget)
        self.newBtn.setGeometry(50, 330, 50, 50)
        self.newBtn.setCursor(Qt.PointingHandCursor)
        self.newBtn.setStyleSheet("QPushButton{image: url('Icons/new.png'); background:transparent;}" 
                                     "QPushButton:hover{image: url('Icons/newhov.png');}")
        
        self.saveBtn = QPushButton(self.centralWidget)
        self.saveBtn.setGeometry(50, 400, 50, 50)
        self.saveBtn.setCursor(Qt.PointingHandCursor)
        self.saveBtn.setStyleSheet("QPushButton{image: url('Icons/save.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/savehov.png');}")
    
        self.openBtn = QPushButton(self.centralWidget)
        self.openBtn.setGeometry(50, 470, 50, 50)
        self.openBtn.setCursor(Qt.PointingHandCursor)
        self.openBtn.setStyleSheet("QPushButton{image: url('Icons/open.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/openhov.png');}")
    
        self.quitBtn = QPushButton(self.centralWidget)
        self.quitBtn.setGeometry(50, 540, 50, 50)
        self.quitBtn.setCursor(Qt.PointingHandCursor)
        self.quitBtn.setStyleSheet("QPushButton{image: url('Icons/exit.png'); background:transparent;}" 
                                   "QPushButton:hover{image: url('Icons/exithov.png');}")

        self.combo = QComboBox(self)
        self.combo.setCurrentIndex(0)
        self.combo.setGeometry(150, 573, 300, 40)
        self.combo.setStyleSheet("QComboBox{font-size:22px; font-family:Calibri; font-weight:bold; color:#006666; border:2px solid #006666; border-bottom-left-radius:20px; border-bottom-right-radius:20px;}"
        						 "QComboBox::drop-down{subcontrol-origin: padding; subcontrol-position: right; border-left-color: darkgray; width: 50px;border-left-width: 2px;border-left-style: solid; border-left-color:#006666;}"
        						 "QComboBox::down-arrow{image:url(Icons/dott.png);}"
        						 "QComboBox QAbstractItemView {selection-background-color: teal; background-color:transparent;}")
        
        self.combo.setCurrentIndex(0)
        self.combo.setCursor(Qt.PointingHandCursor)

        self.billBtn = QPushButton(self.centralWidget)
        self.billBtn.setGeometry(482, 573, 140, 40)
        self.billBtn.setText("Προσφορές")
        self.billBtn.setCursor(Qt.PointingHandCursor)
        self.billBtn.setStyleSheet("QPushButton{color: white; background-color: #006666; font-size:22px; font-family: Calibri; font-weight: bold; border:2px solid #006666; border-bottom-left-radius:20px; border-bottom-right-radius:20px;}"
                                "QPushButton:hover{background-color: white; color: #006666; }")

        
        self.pros = billForm()
        self.newClient = newClient()
        self.warningWindow = warningWindow()
        self.closeWindow = closeWindow()
        self.openCl = openClient()
        self.updateCl = updateClient()


        self.addBtn.clicked.connect(self.addRow)
        self.copyBtn.clicked.connect(self.copyRow)
        self.removeBtn.clicked.connect(self.removeRow)
        self.newBtn.clicked.connect(self.addClient)
        self.openBtn.clicked.connect(self.openClient)
        self.saveBtn.clicked.connect(self.updateTable)
        self.quitBtn.clicked.connect(self.quit)
        self.table.itemSelectionChanged.connect(self.addData)
        self.billBtn.clicked.connect(self.openBill)

        self.newClient.send.connect(self.addNewClient)
        self.closeWindow.closeSend.connect(self.quitApp)
        self.openCl.findSend.connect(self.findClient)
        self.openCl.removeSend.connect(self.removeClient)
        self.updateCl.saveSend.connect(self.saveTable)

        self.combo.currentIndexChanged.connect(self.dateChange)
       
        self.show()

    def addData(self):
        
        total = 0
        row = self.table.currentRow()
        column = self.table.currentColumn()
        rows = self.table.rowCount()

        if self.table.item(row, 2) and self.table.item(row, 3) and column == 4:
            t = self.table.item(row, 2).text()
            p = self.table.item(row, 3).text()
            try:
                float(t)
                float(p)
                to = float(t)-float(p)
                to = str('%.2f' % to)
                self.table.setItem(row, 4, QTableWidgetItem(to))
            except ValueError:
                status = 1
                self.warningWindow.openWarningWindow(status)
        
        for i in range(0, rows):
            if self.table.item(i, 4):
                item = self.table.item(i, 4).text()
                total += float(item)
                
        tot = str('%.2f' % total)
        self.price.setText(tot)
        total = 0

        for i in range(0, rows):
            if self.table.item(i, 3):
                item = self.table.item(i, 3).text()
                total += float(item)
                
        tot = str('%.2f' % total)
        self.total2.setText(tot)
        total = 0

        for i in range(0, rows):
            if self.table.item(i, 2):
                item = self.table.item(i, 2).text()
                total += float(item)
                
        tot = str('%.2f' % total)
        self.total1.setText(tot)
        total = 0
                
    def addRow(self):
        currentRow = self.table.currentRow()
        self.table.insertRow(currentRow+1)

    def copyRow(self):
        row = self.table.currentRow()
        
        data = []
        for i in range(0,5):
            item = self.table.item(row, i)

            if item:
                item = self.table.item(row, i).text()
                data.append(item) 
            else:
                data.append('')
                  
        self.addRow()
        row += 1

        for i in range(0,5):
            itemCopy = data[i]
            self.table.setItem(row, i, QTableWidgetItem(itemCopy))

    def removeRow(self):
        currentRow = self.table.currentRow()
        self.table.removeRow(currentRow)

    def addClient(self):
        self.newClient.show()
        self.newClient.raise_()
            
    def addNewClient(self, na, af, ph):

        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS CUSTOMER(cNAME TEXT PRIMARY KEY, AFM TEXT, PHONE TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS INVOICE(iNAME TEXT, DAT TEXT, ISSUE TEXT, TOTAL TEXT, PAYED TEXT, TOPAY TEXT, FOREIGN KEY(iNAME) REFERENCES CUSTOMER(cNAME))')
        c.execute('INSERT INTO CUSTOMER(cNAME, AFM, PHONE) VALUES(?,?,?)', (na, af, ph))
        
        self.name.setText(na)
        self.afm.setText(af)
        self.phone.setText(ph)
        self.combo.clear()

        conn.commit()
        conn.close()

    def openClient(self):
        self.openCl.show()
        self.openCl.raise_()
        self.openCl.chooseClient()

    def findClient(self, name):
        self.combo.clear()

        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        c.execute('SELECT AFM, PHONE FROM CUSTOMER WHERE cNAME=?', (name,))
        cl = c.fetchone()

        if cl != None:
            cla = cl[0]
            clp = cl[1]
            self.name.setText(name)
            self.afm.setText(cla)
            self.phone.setText(clp)

            c.execute('SELECT DAT,ISSUE,TOTAL,PAYED,TOPAY FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))
            dat = c.fetchall()

            c.execute('SELECT DAT FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))
            idc = c.fetchall()

            if len(idc) == 0:
                self.table.setRowCount(0)
                self.table.insertRow(0)

            else:
                self.table.setRowCount(0)

                for row, rowdata in enumerate(dat):
                    self.table.insertRow(row)
                    
                    for column, data in enumerate(rowdata):
                        
                        self.table.setItem(row, column , QTableWidgetItem(str(data)))

            self.combo.addItem("        All the dates")

            for i in enumerate(idc):
                add = str(idc[i[0]][0])
                self.combo.addItem(add)

            self.table.setHorizontalHeaderLabels(self.colLabels)             
            self.horizHeader.setResizeMode(1, QHeaderView.Stretch)
            self.horizHeader.setResizeMode(0, QHeaderView.Stretch)

        else:
            status = 3
            self.warningWindow.openWarningWindow(status)

        conn.commit()
        conn.close()

    def removeClient(self, name):
        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        c.execute('DELETE FROM CUSTOMER WHERE cNAME=?', (name,))
        c.execute('DELETE FROM INVOICE WHERE iNAME=?', (name,))
        c.execute('DELETE FROM BILL WHERE bNAME=?', (name,))

        conn.commit()
        conn.close()

        self.openCl.chooseClient()

    def updateTable(self):
        self.updateCl.show()
        self.updateCl.raise_()

    def saveTable(self, save):
        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        if not self.name.text():
            status = 4
            self.warningWindow.openWarningWindow(status)
        else:
            name = self.name.text()
            if save == 1:
                c.execute('DELETE FROM INVOICE WHERE iNAME=?',(name,))

                lists = []
                for row in range(self.table.rowCount()):
                    rowdata = []
                    rowdata.append(name)
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                  
                        if len(rowdata) == 6:
                            lists.append(rowdata)
        
                c.executemany('INSERT INTO INVOICE VALUES(?,?,?,?,?,?)', lists)

                c.execute('SELECT DAT FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))
                idc = c.fetchall()

                self.combo.clear()
                self.combo.addItem("        All the dates")
                for i in enumerate(idc):
                    add = str(idc[i[0]][0])
                    self.combo.addItem(add)
                self.table.clearContents()

                if len(idc) == 0:
                    self.table.setRowCount(0)
                    self.table.insertRow(0)
                else:
                    self.table.setRowCount(0)
                
                self.table.clearContents()

                info = c.execute('SELECT DAT,ISSUE,TOTAL,PAYED,TOPAY FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))    
                for row, rowdata in enumerate(info):
                    self.table.insertRow(row)
                    for column, data in enumerate(rowdata):
                        self.table.setItem(row, column , QTableWidgetItem(str(data)))

            else:
                pass

        conn.commit()
        conn.close()

    def dateChange(self):
        conn = connect('Data/Database.db', detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        name = self.name.text()
        c.execute('SELECT DAT FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))
        idc = c.fetchall()

        if self.combo.currentText() == "        All the dates":

            if len(idc) == 0:
                self.table.setRowCount(0)
                self.table.insertRow(0)
            else:
                self.table.setRowCount(0)
                
            self.table.clearContents()
            info = c.execute('SELECT DAT,ISSUE,TOTAL,PAYED,TOPAY FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))    
            for row, rowdata in enumerate(info):
                self.table.insertRow(row)
                for column, data in enumerate(rowdata):
                    self.table.setItem(row, column , QTableWidgetItem(str(data)))
        
            self.table.setHorizontalHeaderLabels(self.colLabels)                
            self.horizHeader.setResizeMode(1, QHeaderView.Stretch)
            self.horizHeader.setResizeMode(0, QHeaderView.Stretch)
            

        else:
            self.table.clearContents()
        
            ct = self.combo.currentText()
            eq = False
            
            if len(idc) == 0:
                self.table.setRowCount(0)
                self.table.insertRow(0)
            else:
                self.table.setRowCount(0)
            
            info = c.execute('SELECT DAT,ISSUE,TOTAL,PAYED,TOPAY FROM INVOICE WHERE iNAME=? ORDER BY DAT',(name,))    
            for row, rowdata in enumerate(info):
                self.table.insertRow(row)
                if rowdata[0] == ct and eq == False:
                    eq = True
                    for column, data in enumerate(rowdata):
                        self.table.setItem(row, column , QTableWidgetItem(str(data)))   
                elif eq == True:
                    for column, data in enumerate(rowdata):
                        self.table.setItem(row, column , QTableWidgetItem(str(data)))

            self.table.setHorizontalHeaderLabels(self.colLabels)                
            self.horizHeader.setResizeMode(1, QHeaderView.Stretch)
            self.horizHeader.setResizeMode(0, QHeaderView.Stretch)
            
        conn.commit()
        conn.close()

    def openBill(self):
        self.pros.combo.clear()
        if self.name.text() and self.afm.text() and self.phone.text():
            self.pros.show()
            self.pros.raise_()
        else:
            status = 4
            self.warningWindow.openWarningWindow(status)
        
        self.pros.name.setText(self.name.text())
        self.pros.afm.setText(self.afm.text())
        self.pros.phone.setText(self.phone.text())
        self.pros.table.clearContents()
        self.pros.combo.addItem("    Choose a date")

        conn = connect("Data/Database.db", detect_types=PARSE_DECLTYPES)
        c = conn.cursor()

        c.execute('SELECT DAT FROM BILL WHERE bNAME=? ORDER BY DAT',(self.name.text(),))
        idc = c.fetchall()

        list = []
        for i in enumerate(idc):
            seen = set(list)
            add = str(idc[i[0]][0])
            if add not in seen:
                list.append(add)

        self.pros.combo.addItems(list)

        conn.commit()
        conn.close()
        
            

    def quit(self):
        close = 1
        self.closeWindow.quit(close)

    def quitApp(self, quit):
        if quit == 1:
            self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
    
  

