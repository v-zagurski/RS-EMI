import sys
import os
import datetime
import locale
import warnings
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

import matplotlib; matplotlib.use('QtAgg')
import matplotlib.ticker as ticker
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from emiwindow import Ui_EmiWindow
from scanwindow import Ui_Settings
from axgroup import AxesGroupBox
from canvas import MplCanvas, NavigationToolbar2QT
from styler import styler, alert, success

from RsSpectrumAnalyzer import RsSpectrumAnalyzer

warnings.filterwarnings("ignore")
basedir = os.getcwd()

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
match os.name == 'nt':
    case True:
        fnt = 'Times New Roman'
    case False:
        fnt = 'Liberation Serif'
matplotlib.rcParams['font.serif'] = [fnt]
np.set_printoptions(precision = 4)

check_list = [0]; nc = 0
data_set = pd.DataFrame(data=np.full(shape=(1, 8), fill_value=''))
data_cal = None; data_cor = None; data_norm = None
fname_set = None; fname_cal = None
fname_cor = None; fname_norm = None
fstart = None; fstop = None; n = None
rbw = None; t = None; det = None
pre = None; att = None
v_freq = [0.009, 0.02, 0.05, 0.15]
v_val1 = np.full(shape = len(v_freq), fill_value = np.nan)
v_val2 = np.full(shape = len(v_freq), fill_value = np.nan)
v_val3 = np.full(shape = len(v_freq), fill_value = np.nan)
v_cal = np.full(shape = len(v_freq), fill_value = 0)
v_cor = np.full(shape = len(v_freq), fill_value = 0)

san = None

def show_error(in1, in2, in3):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setWindowIcon(QtGui.QIcon(basedir + '/res/init.ico'))
    msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(f"{in1}")
    msg_box.setText(f"Ошибка! {in2}")
    QtCore.QTimer.singleShot(3000, msg_box.close)
    msg_box.exec()

def interext(in1, in2, in3):
    inter = interp1d(in2, in3, kind = 'quadratic', fill_value = 'extrapolate')
    return inter(in1)

class CoreThread(QtCore.QThread):
    progress = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self._running = True
        self.core_work()

    def core_work(self):
        while self._running:
            QtCore.QThread.sleep(1)
            _, data, called = san.get_data()
            self.progress.emit((len(data)/n*100, data, called))
            if called:
                return

    def stop(self):
        self._running = False

class EmiScanWindow(QtWidgets.QDialog, Ui_Settings):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowOpacity(0.98)
        self.setFixedSize(702, 260)
        self.setWindowTitle("RS-EMI")
        self.setWindowIcon(QtGui.QIcon(basedir + '/res/init.ico'))

        for i, row in data_set.iterrows():
            for j in range(self.tbl_scan.columnCount()):
                self.tbl_scan.setItem(i, j, QtWidgets.QTableWidgetItem(str(data_set.values[i, j])))
        self.b_load.clicked.connect(self.loadsettings)
        self.b_apply.clicked.connect(self.applysettings)
        self.b_save.clicked.connect(self.savetonew)
        if 0 in check_list: self.ch_0.setChecked(True)
        if 1 in check_list: self.ch_1.setChecked(True)
        if 2 in check_list: self.ch_2.setChecked(True)
        if 3 in check_list: self.ch_3.setChecked(True)

    def loadsettings(self):
        global check_list, nc, fname_set, data_set
        nc = 0
        fname_set, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выберите файл set.xlsx', basedir +
            '/Настройки сканирования', filter = 'Excel files (*set.xlsx)')
        if fname_set:
            data_set = pd.read_excel(fname_set, index_col = None, header = None, dtype = str)
            for i, row in data_set.iterrows():
                for j in range(self.tbl_scan.columnCount()):
                    self.tbl_scan.setItem(i, j, QtWidgets.QTableWidgetItem(str(data_set.values[i, j])))

    def applysettings(self):
        global check_list, nc, data_set, fstart, fstop, n, rbw, t, det, pre, att
        global v_freq, v_val1, v_val2, v_val3, v_cal, v_cor
        check_list = []; nc = 0
        if self.ch_0.isChecked(): check_list.append(0)
        if self.ch_1.isChecked(): check_list.append(1)
        if self.ch_2.isChecked(): check_list.append(2)
        if self.ch_3.isChecked(): check_list.append(3)
        print(check_list)
        for i, row in data_set.iterrows():
            for j in range(self.tbl_scan.columnCount()):
                data_set.iloc[i, j] = self.tbl_scan.item(i, j).text()
        # print(data_set)
        det = data_set.values[check_list[nc], 5]
        fstart = float(data_set.values[check_list[nc], 0])
        fstop = float(data_set.values[check_list[nc], 1])
        rbw = float(data_set.values[check_list[nc], 3])
        n = int(data_set.values[check_list[nc], 2])
        t = float(data_set.values[check_list[nc], 4])
        if data_set.values[check_list[nc], 6] == '0':
            pre = 0
        else:
            pre = 1
        att = int(data_set.values[check_list[nc], 7])
        if san is not None:
            san.setup_meas(det=det, cispr=True, fstart=fstart, fstop=fstop,
                            rbw=rbw, points=n, t=t,
                            att=att, gain=pre)
        v_freq = []
        for i in range(len(check_list)):
            v_freq = np.append(v_freq,
                                np.linspace(float(data_set.values[check_list[i], 0]),
                                            float(data_set.values[check_list[i], 1]),
                                            int(data_set.values[check_list[i], 2])+1))
        v_val1 = np.full(shape = len(v_freq), fill_value = np.nan)
        v_val2 = np.full(shape = len(v_freq), fill_value = np.nan)
        v_val3 = np.full(shape = len(v_freq), fill_value = np.nan)
        v_cal = np.full(shape = len(v_freq), fill_value = 0)
        v_cor = np.full(shape = len(v_freq), fill_value = 0)

        self.close()

    def savetonew(self):
        global fname_set, data_set
        fname_set, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Укажите имя файла', filter = 'Excel files (*.xlsx)')
        if fname_set:
            for i, row in data_set.iterrows():
                for j in range(self.tbl_scan.columnCount()-1):
                    data_set.iloc[i, j] = self.tbl_scan.item(i, j).text()
            data_set.to_excel(fname_set, index = False, header = False)

class EmiWindow(QtWidgets.QDialog, Ui_EmiWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setFixedSize(1240, 650)
        self.setWindowOpacity(0.98)
        self.setWindowTitle("RS-EMI")
        self.setWindowIcon(QtGui.QIcon(basedir + '/res/init.ico'))

        self.corethread = CoreThread()
        self.corethread.progress.connect(self.update_work)

        try:
            with open(basedir + '/inst.ini', 'r') as instfile:
                for line in instfile:
                    st = line.strip()
            self.f_inst.setText(st)
        except:
            self.f_inst.setText('TCPIP::')

        self.v_fnorm = [0.009, 0.15, 0.5, 6, 30, 100, 1000]
        self.v_vnorm = np.full(shape = len(self.v_fnorm), fill_value = np.nan)
        self.fk = v_freq; self.fl = v_freq;
        self.l = np.full(shape = len(v_freq), fill_value = 0)
        self.k = np.full(shape = len(v_freq), fill_value = 0)

        self.sc = MplCanvas(self, dpi = 100)
        self.ylb = 'Напряжение ИРП, дБмкВ'
        self.tlb = NavigationToolbar2QT(self.sc)
        plotlayout = QtWidgets.QGridLayout()
        plotlayout.addWidget(self.tlb)
        plotlayout.addWidget(self.sc)
        self.gr_plot.setLayout(plotlayout)
        self.gr_ax = AxesGroupBox(self.gr_plot)
        self.gr_ax.setGeometry(330, 18, 320, 58)
        self.gr_ax.sp_ymin.setValue(0)
        self.gr_ax.sp_ymax.setValue(80)
        self.plotdata()

        self.b_connect.clicked.connect(self.visaconnect)
        self.cmb_val.currentIndexChanged.connect(self.setval)
        self.b_settings.clicked.connect(lambda: self.setmeas(0))
        self.b_calib.clicked.connect(lambda: self.setmeas(1))
        self.b_corr.clicked.connect(lambda: self.setmeas(2))
        self.b_norm.clicked.connect(lambda: self.setmeas(3))
        self.ch_calib.stateChanged.connect(lambda: self.setused(0))
        self.ch_corr.stateChanged.connect(lambda: self.setused(1))
        self.ch_norm.stateChanged.connect(lambda: self.setused(2))
        self.sp_att.valueChanged.connect(self.setatt)
        self.b_start.clicked.connect(self.start_corethread)
        self.gr_ax.cmb_xmin.currentIndexChanged.connect(self.setx)
        self.gr_ax.cmb_xmax.currentIndexChanged.connect(self.setx)
        self.gr_ax.sp_ymin.valueChanged.connect(self.sety)
        self.gr_ax.sp_ymax.valueChanged.connect(self.sety)
        self.b_clear.clicked.connect(self.clearval)
        self.b_xls.clicked.connect(self.savexls)
        self.b_jpg.clicked.connect(self.savejpg)
        self.b_xls_l.clicked.connect(self.loadxls)
        # self.b_csv_l.clicked.connect(self.loadcsv)

    def visaconnect(self):
        global san
        match self.b_connect.isChecked():
            case True:
                try:
                    self.setCursor(Qt.CursorShape.WaitCursor)
                    san = RsSpectrumAnalyzer(self.f_inst.text())
                    self.setCursor(Qt.CursorShape.ArrowCursor)
                    success(self.f_inst, True)
                    san.setup_display(unit='DBUV', ref=90, scale=100)
                    san.setup_meas(trac_mode='MAXH', cont=0, av_num=1)
                    self.f_stat.setText(san._status)
                    self.dispreg()
                except:
                    self.setCursor(Qt.CursorShape.ArrowCursor)
                    alert(self.f_inst, True)
            case False:
                try:
                    san.close()
                    san = None
                except: pass
                alert(self.f_inst, False)
                self.b_start.setChecked(False)
                self.f_stat.setText(' ')
                self.dispreg()

    def setval(self):
        match self.cmb_val.currentIndex():
            case 0:
                self.ylb = 'Напряжение ИРП, дБмкВ'
            case 1:
                self.ylb = 'Напряженость поля ИРП, дБмкВ/м'
            case 2:
                self.ylb = 'Сила тока ИРП, дБмкА'
        self.plotdata()

    def setmeas(self, inp):
        match inp:
            case 0:
                sw = EmiScanWindow()
                sw.exec()
                match fname_set is not None:
                    case True:
                        self.f_settings.setText(os.path.basename(fname_set))
                    case False:
                        self.f_settings.setText('Пользовательские настройки')
            case 1:
                global fname_cal, data_cal, v_cal
                fname_cal, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл cal.xlsx',
                    basedir + '/Калибровочные коэф-ты',
                    filter = 'Excel files (*cal.xlsx)')
                if fname_cal:
                    data_cal = pd.read_excel(fname_cal)
                    self.fk = data_cal['f'].values[:]; self.k = data_cal['k'].values[:]
                    v_cal = interext(v_freq, self.fk, self.k)
                    self.f_calib.setText(os.path.basename(fname_cal))
                    self.ch_calib.setChecked(True)
            case 2:
                global fname_cor, data_cor, v_cor
                fname_cor, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл cor.xlsx',
                    basedir + '/Амплитудная коррекция',
                    filter = 'Excel files (*cor.xlsx)')
                if fname_cor:
                    data_cor = pd.read_excel(fname_cor)
                    self.fl = data_cor['f'].values[:]; self.l = data_cor['l'].values[:]
                    v_cor = interext(v_freq, self.fl, self.l)
                    self.f_corr.setText(os.path.basename(fname_cor))
                    self.ch_corr.setChecked(True)
            case 3:
                global fname_norm, data_norm
                fname_norm, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл nor.xlsx',
                    basedir + '/Нормы',
                    filter = 'Excel files (*nor.xlsx)')
                if fname_norm:
                    data_norm = pd.read_excel(fname_norm)
                    self.v_fnorm = data_norm['f'].values[:]; self.v_vnorm = data_norm['a'].values[:]
                    self.f_norm.setText(os.path.basename(fname_norm))
                    self.ch_norm.setChecked(True)
        self.plotdata()

    def setused(self, inp):
        global v_cal, v_cor
        match inp:
            case 0:
               if self.ch_calib.isChecked():
                   self.fk = data_cal['f'].values[:]; self.k = data_cal['k'].values[:]
                   v_cal = interext(v_freq, self.fk, self.k)
               else:
                   v_cal = np.full(shape = len(v_freq), fill_value = 0)
            case 1:
                if self.ch_corr.isChecked():
                    self.fl = data_cor['f'].values[:]; self.l = data_cor['l'].values[:]
                    v_cor = interext(v_freq, self.fl, self.l)
                else:
                    v_cor = np.full(shape = len(v_freq), fill_value = 0)
            case 2:
                if self.ch_norm.isChecked():
                    self.v_fnorm = data_norm['f'].values[:]; self.v_vnorm = data_norm['a'].values[:]
                else:
                  self.v_vnorm = np.full(shape = len(self.v_fnorm), fill_value = np.nan)
        self.plotdata()

    def setatt(self):
        self.plotdata()

    def start_corethread(self):
        if san is not None:
            match self.b_start.isChecked():
                case True:
                    san.initiate()
                    self.corethread.start()
                    self.b_connect.setEnabled(False)
                case False:
                    san.stop()
                    self.finish_work()

    def update_work(self, inp):
        global v_val1, v_val2, v_val3
        self.progressBar.setValue(round(inp[0]))
        ind = np.argmax(v_freq >= fstart)
        match self.cmb_trac.currentIndex():
            case 0:
                v_val1[ind:ind+len(inp[1])] = inp[1]
            case 1:
                v_val2[ind:ind+len(inp[1])] = inp[1]
            case 2:
                v_val3[ind:ind+len(inp[1])] = inp[1]
        self.f_stat.setText(san._status)
        self.dispreg()
        self.plotdata()
        if inp[2]:
            if self.b_csv.isChecked():
                file = 'tr'+str(self.cmb_trac.currentIndex()+1)+'n'+str(nc)+ \
                    '-'+str(datetime.datetime.now())[:19].replace(':','-')
                san.save_data(file)
            if self.b_scr.isChecked():
                file = 'tr'+str(self.cmb_trac.currentIndex()+1)+'n'+str(nc)+ \
                    '-'+str(datetime.datetime.now())[:19].replace(':','-')
                san.save_screen(file)
            QtCore.QThread.sleep(2)
            self.add_work()

    def add_work(self):
        global nc, fstart, fstop, n, rbw, t, det, pre, att
        nc = nc+1
        try:
            det = data_set.values[check_list[nc], 5]
            fstart = float(data_set.values[check_list[nc], 0])
            fstop = float(data_set.values[check_list[nc], 1])
            rbw = float(data_set.values[check_list[nc], 3])
            n = int(data_set.values[check_list[nc], 2])
            t = float(data_set.values[check_list[nc], 4])
            if data_set.values[check_list[nc], 6] == '0':
                pre = 0
            else:
                pre = 1
            att = int(data_set.values[check_list[nc], 7])
            if san is not None:
                san.setup_meas(det=det, cispr=True, fstart=fstart, fstop=fstop,
                                rbw=rbw, points=n, t=t,
                                att=att, gain=pre)
                san.setup_meas(det=det, cispr=True, fstart=fstart, fstop=fstop,
                                rbw=rbw, points=n, t=t,
                                att=att, gain=pre)
            self.start_corethread()
        except:
            self.finish_work()
            nc = 0
            det = data_set.values[check_list[nc], 5]
            fstart = float(data_set.values[check_list[nc], 0])
            fstop = float(data_set.values[check_list[nc], 1])
            rbw = float(data_set.values[check_list[nc], 3])
            n = int(data_set.values[check_list[nc], 2])
            t = float(data_set.values[check_list[nc], 4])
            if data_set.values[check_list[nc], 6] == '0':
                pre = 0
            else:
                pre = 1
            att = int(data_set.values[check_list[nc], 7])
            if san is not None:
                san.setup_meas(det=det, cispr=True, fstart=fstart, fstop=fstop,
                                rbw=rbw, points=n, t=t,
                                att=att, gain=pre)

    def finish_work(self):
        self.corethread.stop()
        self.b_connect.setEnabled(True)
        self.b_start.setChecked(False)
        self.progressBar.setValue(0)
        self.f_stat.setText(san._status)
        self.dispreg()

    def dispreg(self):
        if san is not None:
            esr = san._esr
            if 0 in esr:
                success(self.f_opc, True)
            else:
                success(self.f_opc, False)
            if any(value in [3, 4, 5] for value in esr):
                alert(self.f_qye, True)
            else:
                alert(self.f_qye, False)
        else:
            success(self.f_opc, False)
            success(self.f_qye, False)

    def clearval(self):
        global v_val1, v_val2, v_val3
        v_val1 = np.full(shape = len(v_freq), fill_value = np.nan)
        v_val2 = np.full(shape = len(v_freq), fill_value = np.nan)
        v_val3 = np.full(shape = len(v_freq), fill_value = np.nan)
        self.plotdata()

    def savexls(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Укажите имя файла', basedir + '/Результаты сканирования',
            filter = 'Excel files (*.xlsx)')
        if fname:
            match self.cmb_val.currentIndex():
                case 0:
                    datf = pd.DataFrame({'freq, MHz': v_freq, 'val1, unit': v_val1,
                                            'val2, unit': v_val2, 'val3, unit': v_val3,
                                            'unit': 'dBuV'})
                case 1:
                    datf = pd.DataFrame({'freq, MHz': v_freq, 'val1, unit': v_val1,
                                            'val2, unit': v_val2, 'val3, unit': v_val3,
                                            'unit': 'dBuV/m'})
                case 2:
                    datf = pd.DataFrame({'freq, MHz': v_freq, 'val1, unit': v_val1,
                                            'val2, unit': v_val2, 'val3, unit': v_val3,
                                            'unit': 'dBuA'})
            datf.to_excel(fname, index = False)

    def savejpg(self):
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Укажите имя файла', basedir + '/Результаты сканирования/Изображения',
            filter = 'JPEG files (*.jpg)')
        if fname:
            self.sc.print_jpg(fname)

    def loadxls(self):
        global v_freq, v_val1, v_val2, v_val3, v_cal, v_cor
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Выберите файл .xlsx', basedir + '/Результаты сканирования',
            filter = 'Excel files (*.xlsx)')
        if fname:
            datf = pd.read_excel(fname)
            v_freq = datf['freq, MHz'].values[:]
            v_val1 = datf['val1, unit'].values[:]
            v_val2 = datf['val2, unit'].values[:]
            v_val3 = datf['val3, unit'].values[:]
            unit = datf['unit'].values[0]
            v_cal = interext(v_freq, self.fk, self.k)
            v_cor = interext(v_freq, self.fl, self.l)
            match unit:
                case 'dBuV':
                    self.cmb_val.setCurrentIndex(0)
                    self.ylb = 'Напряжение ИРП, дБмкВ'
                case 'dBuV/m':
                    self.cmb_val.setCurrentIndex(1)
                    self.ylb = 'Напряженность поля ИРП, дБмкВ/м'
                case 'dBuA':
                    self.cmb_val.setCurrentIndex(2)
                    self.ylb = 'Сила тока ИРП, дБмкА'
            self.plotdata()

    def setx(self):
        if float(self.gr_ax.cmb_xmin.currentText()) < float(self.gr_ax.cmb_xmax.currentText()):
            self.plotdata()

    def sety(self):
        if self.gr_ax.sp_ymin.value() < self.gr_ax.sp_ymax.value():
            self.plotdata()

    def plotdata(self):
        self.sc.axes.cla()
        self.sc.axes.ticklabel_format(useLocale = True)
        line3, = self.sc.axes.plot(v_freq, v_val3+v_cal+v_cor+self.sp_att.value(),
                            linewidth = 1.5, alpha = 0.85, color = (0.46, 0.67, 0.19))
        line1, = self.sc.axes.plot(v_freq, v_val1+v_cal+v_cor+self.sp_att.value(),
                            linewidth = 1.5, alpha = 0.85, color = (0.85, 0.32, 0.1))
        line2, = self.sc.axes.plot(v_freq, v_val2+v_cal+v_cor+self.sp_att.value(),
                            linewidth = 1.5, alpha = 0.85, color = (0.49, 0.18, 0.56))
        line4, = self.sc.axes.plot(self.v_fnorm, self.v_vnorm, linewidth = 2.5,
                                    color = '#5580aa')
        self.sc.axes.set(xscale = 'log')
        self.sc.axes.set_ylabel(self.ylb, fontname = fnt, fontsize = 18)
        self.sc.axes.set_xlabel('Частота, МГц', fontname = fnt, fontsize = 18)
        self.sc.axes.yaxis.set_major_locator(ticker.MultipleLocator(10))
        self.sc.axes.xaxis.set_ticks(np.array([0.009, 0.02, 0.05, 0.15, 0.5,
                                                1, 2, 5, 10, 15, 30, 50, 100, 200, 500, 1000,
                                                3000, 9000, 18000]))
        self.sc.axes.set_xticklabels(['0,009', '0,02', '0,05', '0,15', '0,5',
                                        '1', '2', '5', '10', '15', '30', '50', '100', '200', '500',
                                        f'1∙10\N{SUPERSCRIPT THREE}', f'3∙10\N{SUPERSCRIPT THREE}',
                                        f'9∙10\N{SUPERSCRIPT THREE}', f'18∙10\N{SUPERSCRIPT THREE}'])
        self.sc.axes.tick_params(labelsize = 14, labelfontfamily = 'serif')
        self.sc.axes.tick_params(axis = 'x', which = 'minor', labelcolor = 'white')
        self.sc.axes.set_ylim([self.gr_ax.sp_ymin.value(), self.gr_ax.sp_ymax.value()])
        self.sc.axes.set_xlim([float(self.gr_ax.cmb_xmin.currentText()),
                                float(self.gr_ax.cmb_xmax.currentText())])
        self.sc.axes.grid(True)
        self.sc.axes.format_coord = lambda x, y: "x = {:4.3F}\n y = {:3.2f}".format(x, y)
        if np.any(~np.isnan(v_val1)):
            line1.set_label('Уровень ИРП')
        if np.any(~np.isnan(v_val2)):
            line2.set_label('Уровень ИРП 2')
        if np.any(~np.isnan(v_val3)):
            line3.set_label('Уровень фона')
        if np.any(~np.isnan(self.v_vnorm)):
            line4.set_label('Норма по ГОСТ')
        self.sc.axes.legend(prop = {'family': 'serif', 'size': 14})
        self.sc.draw()

    def closeEvent(self, event):
        if san is not None:
            san.close()
            self.corethread.terminate()

# sys.excepthook = show_error

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()

styler(app)

ew = EmiWindow()
ew.show()

sys.exit(app.exec())
