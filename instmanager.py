# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 15:02:35 2025

@author: user
"""

import threading
import pyvisa, pyvisa_py

class InstrumentManager:
    def __init__(self):
        self._lock = threading.RLock()
        self._instruments = {}
        self._res_manager = None

    def get_res_manager(self):
        with self._lock:
            if self._res_manager is None:
                self._res_manager = pyvisa.ResourceManager('@py')
            return self._res_manager

    def open_inst(self, res_string, thread_id=None):
        if thread_id is None:
            thread_id = threading.current_thread().ident

        key = f"{res_string}_{thread_id}"

        with self._lock:
            if key not in self._instruments:
                rm = self.get_res_manager()
                inst = rm.open_resource(res_string)
                self._instruments[key] = inst

            return self._instruments[key]

    def close_inst(self, res_string, thread_id=None):
        if thread_id is None:
            thread_id = threading.current_thread().ident

        key = f"{res_string}_{thread_id}"

        with self._lock:
            if key in self._instruments:
                self._instruments[key].close()
                del self._instruments[key]

    def close_all(self):
        with self._lock:
            for instrument in self._instruments.values():
                try:
                    instrument.close()
                except:
                    pass
            self._instruments.clear()

# manager = InstrumentManager()
