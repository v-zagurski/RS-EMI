from PySide6.QtCore import (QCoreApplication, QRect)
from PySide6.QtWidgets import (QCheckBox, QFrame, QGroupBox,
                               QTableWidgetItem)
from _gui.mytable import MyTableWidget
from _gui.mybutton import MyPushButton

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(702, 260)
        self.gr_set = QGroupBox(Settings)
        self.gr_set.setObjectName(u"gr_set")
        self.gr_set.setGeometry(QRect(10, 10, 681, 201))
        self.tbl_scan = MyTableWidget(self.gr_set)
        if (self.tbl_scan.columnCount() < 8):
            self.tbl_scan.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tbl_scan.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.tbl_scan.rowCount() < 4):
            self.tbl_scan.setRowCount(4)
        self.tbl_scan.setObjectName(u"tbl_scan")
        self.tbl_scan.setGeometry(QRect(10, 30, 641, 155))
        self.tbl_scan.setFrameShape(QFrame.Shape.Box)
        self.tbl_scan.setFrameShadow(QFrame.Shadow.Plain)
        self.tbl_scan.horizontalHeader().setDefaultSectionSize(77)
        self.tbl_scan.verticalHeader().setDefaultSectionSize(30)
        self.ch_0 = QCheckBox(self.gr_set)
        self.ch_0.setObjectName(u"ch_0")
        self.ch_0.setGeometry(QRect(653, 64, 21, 20))
        self.ch_1 = QCheckBox(self.gr_set)
        self.ch_1.setObjectName(u"ch_1")
        self.ch_1.setGeometry(QRect(653, 94, 21, 20))
        self.ch_2 = QCheckBox(self.gr_set)
        self.ch_2.setObjectName(u"ch_2")
        self.ch_2.setGeometry(QRect(653, 124, 21, 20))
        self.ch_3 = QCheckBox(self.gr_set)
        self.ch_3.setObjectName(u"ch_3")
        self.ch_3.setGeometry(QRect(653, 154, 21, 20))
        self.b_load = MyPushButton(Settings)
        self.b_load.setObjectName(u"b_load")
        self.b_load.setGeometry(QRect(10, 220, 111, 31))
        self.b_load.setCheckable(False)
        self.b_load.setAutoDefault(True)
        self.b_apply = MyPushButton(Settings)
        self.b_apply.setObjectName(u"b_apply")
        self.b_apply.setGeometry(QRect(130, 220, 111, 31))
        self.b_apply.setCheckable(False)
        self.b_save = MyPushButton(Settings)
        self.b_save.setObjectName(u"b_save")
        self.b_save.setGeometry(QRect(250, 220, 151, 31))
        self.b_save.setCheckable(False)

        self.retranslateUi(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Dialog", None))
        self.gr_set.setTitle(QCoreApplication.translate("Settings", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f", None))
        ___qtablewidgetitem = self.tbl_scan.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Settings", u"Fstart", None));
        ___qtablewidgetitem1 = self.tbl_scan.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Settings", u"Fstop", None));
        ___qtablewidgetitem2 = self.tbl_scan.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Settings", u"N", None));
        ___qtablewidgetitem3 = self.tbl_scan.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Settings", u"RBW", None));
        ___qtablewidgetitem4 = self.tbl_scan.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Settings", u"t", None));
        ___qtablewidgetitem5 = self.tbl_scan.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Settings", u"Det", None));
        ___qtablewidgetitem6 = self.tbl_scan.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Settings", u"Amp", None));
        ___qtablewidgetitem7 = self.tbl_scan.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Settings", u"Att", None));
        self.ch_0.setText("")
        self.ch_1.setText("")
        self.ch_2.setText("")
        self.ch_3.setText("")
        self.b_load.setText(QCoreApplication.translate("Settings", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.b_apply.setText(QCoreApplication.translate("Settings", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.b_save.setText(QCoreApplication.translate("Settings", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 \u043d\u043e\u0432\u044b\u0439", None))
