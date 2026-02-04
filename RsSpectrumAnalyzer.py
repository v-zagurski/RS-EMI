# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 08:33:07 2025

@author: user
"""

import numpy as np
# from RsInstrument import RsInstrument
from instmanager import InstrumentManager
im = InstrumentManager()

def regviewer(value):
    pos_array = []; pos=0
    while int(value) >= (1<<pos):
      if int(value) & (1<<pos):
        pos_array.append(pos)
      pos=pos+1
    return pos_array

class RsSpectrumAnalyzer:
    def __init__(self, res_string: str):
        self._str = res_string
        self.core = im.open_inst(self._str)
        self.core.timeout = 2000
        self.core.write_termination, self.core.read_termination = '\n', '\n'
        self.core.query('*ESE?')
        self.core.write('*ESE 61')
        self.core.write('STAT:QUES:POW:ENAB 4')
        self.core.write('INST REC')
        self.core.write('FREQ:MODE SCAN')
        self.core.write('FORM REAL')
        self.core.write('INIT:CONT 0')
        self.core.write('DISP:TRAC:Y:SPAC LOG')
        self._called = False
        self._status = 'Готов к работе.'
        self._idn = self.core.query('*IDN?')
        self._f_ax = (None, None, None)
        self._check_registers()

    def setup_display(self, unit: str = None, ref: int = None, scale: int = None):
        if unit is not None:
            self.core.write('UNIT:POW ' + unit)
        if ref is not None:
            self.core.write(f'DISP:TRAC:Y:RLEV {str(ref)}')
        if scale is not None:
            self.core.write(f'DISP:TRAC:Y:SCAL {str(scale)}')
        self._check_registers()

    def setup_meas(self, trac_mode: str = None, cont: int = None,
                          av_num: int = None,
                          det: str = None, cispr: bool = False,
                          fstart: float = None, fstop: float = None,
                          step: float = None, points: int = None, rbw: float = None,
                          t: float = None, att: int = None, gain: int = None):
        if trac_mode is not None:
            self.core.write(f'DISP:TRAC:MODE {trac_mode}')
        if cont is not None:
            if cont in (0, 1):
                self.core.write(f'INIT:CONT {str(cont)}')
        if av_num is not None:
          self.core.write(f'SWE:COUN {str(av_num)}')
        if det is not None:
            self.core.write(f'DET {det}')
        if fstart is not None:
            self.core.write(f'SCAN:START {str(fstart)} MHz')
        if fstop is not None:
            self.core.write(f'SCAN:STOP {str(fstop)} MHz')
        if step is not None and points is None:
            self.core.write(f'SCAN:STEP {str(step)} kHz')
        if points is not None and fstart is not None:
            step = (fstop-fstart)*1e3/points
            self.core.write(f'SCAN:STEP {str(step)} kHz')
        if rbw is not None:
            match cispr:
                case False:
                    self.core.write(f'BAND {str(rbw)} kHz')
                case True:
                    self.core.write(f'BAND:CISP {str(rbw)} kHz')
        if t is not None:
            self.core.write(f'SWE:TIME {str(t)}')
        if gain is not None:
            if gain in (0, 1):
                self.core.write(f'INP:GAIN {str(gain)}')
        if att is not None:
            self.core.write(f'INP:ATT {str(att)}')
        f1 = float(self.core.query('SCAN:START?'))
        f2 = float(self.core.query('SCAN:STOP?'))
        st = float(self.core.query('SCAN:STEP?'))
        self._f_ax = (f1, st, f2)
        self._check_registers()

    def initiate(self):
        self._called = False
        self._status = 'Сканирование...'
        self.core.write('INIT:IMM')
        self._check_registers()

    def stop(self):
        self.core.write('ABOR')
        self.core.query('*ESR?')
        self._called = True
        self._status = 'Готов к работе.'

    def get_data(self):
        try:
            freqs = np.arange(self._f_ax[0], self._f_ax[2]+self._f_ax[1], self._f_ax[1])
            data = self.core.query_binary_values('TRAC1:DATA?', datatype='f', container=np.array)
            self._check_registers()
            return freqs, data, self._called
        except: return None, None, self._called

    def save_data(self, filename: str):
        if 'Ceyear' in self._idn:
            self.core.write(f'MMEM:STOR:TRAC:DATA TRACE1,"D:\{filename}.csv"')
        else:
            self.core.write('MMEM:STOR:TRAC:DATA TRACE1,' + filename + '.csv')
        self._check_registers()

    def save_screen(self, filename: str):
        if 'Ceyear' in self._idn:
            self.core.write(f'MMEM:STOR:SCR D:\{filename}.bmp')
        else:
            self.core.write('MMEM:STOR:SCR ' + filename + '.bmp')
        self._check_registers()

    def _check_registers(self):
        powval = float(self.core.query('STAT:QUES:POW?'))
        if powval != 0:
            self._called = True
            self._status = 'Опасный уровень сигнала!'

        stbval = float(self.core.query('*STB?'))
        self._stb = regviewer(stbval)
        if 4 in self._stb:
            self._status = 'Доступно сообщение!'

        esrval = float(self.core.query('*ESR?'))
        self._esr = regviewer(esrval)
        if any(value in [2, 3, 4, 5] for value in self._esr):
            err = self.core.query('SYST:ERR?')
            self._status = f'Обнаружена ошибка! {err}'
        if 0 in self._esr:
            self._called = True
            self._status = 'Готов к работе.'

    def close(self):
        im.close_inst(self._str)
