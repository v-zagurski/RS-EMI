import time
from RsSpectrumAnalyzer import RsSpectrumAnalyzer

san = RsSpectrumAnalyzer('TCPIP0::169.254.19.12::inst0::INSTR')
san.setup_display(unit='DBUV', ref=80, scale=100)
san.setup_meas(trac_mode='MAXH', cont=0, av_num=1, det='RMS',
               fstart=20, fstop=50, points=500,
               rbw=100, t=0.01, att=20)
print(san._idn)
print(san._status)
print(san.core.query('FORM?'))

for i in range(10):
    _, _, called = san.get_data()
    print(san._stb)
    print(san._esr)
    time.sleep(3)
    # print(called)

san.close()
