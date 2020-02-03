# for collecting data, 60samples(60seconds) per click

import os
import sys
import time
from os.path import join
from os import listdir

import librosa
import numpy as np
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt


from ctypes import *
import py_bsvml as bv

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtGui import *

newfont = QFont("Helvetica", 30, QFont.Bold)

DATA_FOLDER = 'C:/Users/MAKinteract/makinteract'
as_dir = join(DATA_FOLDER, 'as')
ce_dir = join(DATA_FOLDER, 'ce')
ur_dir = join(DATA_FOLDER, 'ur')

as_arr_dir = join(as_dir, 'arr')
ce_arr_dir = join(ce_dir, 'arr')
ur_arr_dir = join(ur_dir, 'arr')

if not os.path.exists(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)
if not os.path.exists(as_dir):
    os.mkdir(as_dir)
if not os.path.exists(ce_dir):
    os.mkdir(ce_dir)
if not os.path.exists(ur_dir):
    os.mkdir(ur_dir)
if not os.path.exists(ce_arr_dir):
    os.mkdir(ce_arr_dir)
if not os.path.exists(as_arr_dir):
    os.mkdir(as_arr_dir)
if not os.path.exists(ur_arr_dir):
    os.mkdir(ur_arr_dir)
    
SAMPLES = 10000
SAMPLE_RATE = 10000

bsInfo = bv.BitScopeInfo()
bsCount = bv.listBitScopes(1, pointer(bsInfo))
if bsCount == 0:
    exit("Couldn't find a BitScope.")
bs = bv.openBitScope(bsInfo.port)



class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'makinteract data collect'
        self.left = 10
        self.top = 10
        self.width = 1320
        self.height = 1200
        
        
        self.iteration = 60

        ##
        self.atrial = 0
        self.btrial = 0
        self.utrial = 0
        
        try:
            as_cnt = [int(f.split('_')[1]) for f in listdir(as_dir) if f!='arr']
        except:
            as_cnt=[0]
        as_cnt = as_cnt + [0]
        print("starting from as_", max(as_cnt)+1)
        self.atrial += max(as_cnt)
        
        try:
            ce_cnt = [int(f.split('_')[1]) for f in listdir(ce_dir) if f!='arr']
        except:
            ce_cnt = [0]
        ce_cnt=ce_cnt+[0]
        print("starting from ce_", max(ce_cnt)+1)
        self.btrial += max(ce_cnt)
        
        try:
            ur_cnt = [int(f.split('_')[1]) for f in listdir(ur_dir) if f!='arr']
        except:
            ur_cnt = [0]
        ur_cnt=ur_cnt+[0]
        print("starting from ur_", max(ur_cnt)+1)
        self.utrial += max(ur_cnt)
        
        
        self.cur = 'as'

        self.initUI()

    def initUI(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.finish)
        self.countdown = QTimer()
        self.countdown.timeout.connect(self.record)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.start = QPushButton('START', self)
        self.start.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.start.setStyleSheet("background-color: grey")
        self.start.setFont(newfont)
        self.start.move(100,70)
        self.start.clicked.connect(self.start_on_click)

        self.start.setSizePolicy(
        QSizePolicy.Preferred,
        QSizePolicy.Expanding)

        self.aselect = QPushButton('A', self)
        self.aselect.setStyleSheet("background-color: grey")
        self.aselect.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.aselect.setFont(newfont)
        self.aselect.clicked.connect(self.aselect_clicked)

        self.bselect = QPushButton('B', self)
        self.bselect.setStyleSheet("background-color: grey")
        self.bselect.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.bselect.setFont(newfont)
        self.bselect.clicked.connect(self.bselect_clicked)
        
        self.uselect = QPushButton('U', self)
        self.uselect.setStyleSheet("background-color: grey")
        self.uselect.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.uselect.setFont(newfont)
        self.uselect.clicked.connect(self.uselect_clicked)

        select = QVBoxLayout()
        select.addWidget(self.aselect,2)
        select.addWidget(self.bselect,2)
        select.addWidget(self.uselect,2)

        layout = QHBoxLayout()
        layout.addWidget(self.start, 1)
        layout.addLayout(select)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.show()

    @pyqtSlot()
    def start_on_click(self):
        print('PyQt5 button click')
        self.start.setStyleSheet("background-color: red")
        #automatically run record after two seconds
        self.countdown.start(2000)
        

    def record(self):
        
        self.update()   
        self.show()
      
        #duration
        print("record!!")

        self.timer.start(1100*self.iteration - 3000)
        if self.cur == 'as':
            self.atrial += 1
        if self.cur == 'ce':
            self.btrial += 1
        if self.cur == 'ur':
            self.utrial += 1
         
        for i in range(self.iteration):
            self.cur_i = i
            self._record()
        self.countdown.stop()  
        
        
    def _record(self):
        
        outroSize = (int)(SAMPLES/2)
        introSize = (int)(SAMPLES/2)
        totalSize = outroSize + introSize
        bv.mode(bs, bv.SINGLE)
        bv.macro(bs, True)

        bv.enableAnalogueChannel(bs, bv.CHA)
        bv.rate(bs, SAMPLE_RATE)
        bv.traceIntro(bs, introSize)
        bv.traceOutro(bs, outroSize)
        bv.traceDelay(bs, 0) # ms
        bv.traceTimeout(bs, bv.getMinTimeout(bs)) # ms
        bv.trigType(bs, bv.COMP)
        bv.trigChannelEnable(bs, bv.CHA, True)
        bv.trigChannelEdge(bs, bv.CHA, bv.RISE)
        bv.trigLevel(bs, 1.5) # v
        bv.trigIntro(bs, 4) # samples
        bv.trigOutro(bs, 4) # samples
        bv.range(bs, 5.0) # v
        bv.offset(bs, 1.0) # v
        bv.dumpChannel(bs, bv.CHA)
        bv.dumpSize(bs, totalSize)
        bv.updateBitScope(bs)

        byteCount = bv.getBytesInDump(bs)
        rawData = (c_ubyte * byteCount)()
        macroData = (c_short * totalSize)()

        bv.trace(bs)
        bv.address(bs, bv.getIntroStartAddress(bs)) # must be set after trace
        bv.updateBitScope(bs)
        bv.acquire(bs, rawData)

        # convert rawData to 16 bit data
        bv.convertMacroTrace(rawData, macroData, byteCount)

        data = list(macroData)
        # do stuff with data
        #for i in macroData:
        #        print (i)

        print("acquired %d data" % len(data))
        arr = np.array(data,dtype=np.float64)
        ori = arr
        print("before max: ",np.max(arr))
        print("before min: ",np.min(arr))

        #arr = arr - arr.mean(axis=0)
        div = (np.max(arr) - np.min(arr))/2.
        if div == 0:
            div = 1.
        arr = arr / div
        arr = arr - arr.mean(axis=0)
      
        
        #arr = normalize(arr[:,np.newaxis],axis=0).ravel()
        #arr /= np.max(data)
        print("----")
        print(np.max(arr))
        print(np.min(arr))
        print("----")
        S = librosa.feature.melspectrogram(y=arr,sr=SAMPLE_RATE)
        if self.cur == 'as':
            filename = self.cur + '_' + str(self.atrial)+'_'+str(self.cur_i+1)
            arrname = self.cur + '_' + str(self.atrial)+'_'+str(self.cur_i+1)+'_arr'
        elif self.cur == 'ce':
            filename = self.cur + '_' + str(self.btrial)+'_'+str(self.cur_i+1)
            arrname = self.cur + '_' + str(self.btrial)+'_'+str(self.cur_i+1)+'_arr'
        elif self.cur == 'ur':
            filename = self.cur + '_' + str(self.utrial)+'_'+str(self.cur_i+1)
            arrname = self.cur + '_' + str(self.utrial)+'_'+str(self.cur_i+1)+'_arr'
            
        if self.cur == 'as':
            fulldir = join(as_dir, filename)
            arrfulldir = join(as_arr_dir, arrname)
        elif self.cur == 'ce':
            fulldir = join(ce_dir, filename)
            arrfulldir = join(ce_arr_dir, arrname)
        elif self.cur == 'ur':
            fulldir = join(ur_dir, filename)
            arrfulldir = join(ur_arr_dir, arrname)
        else:
            print("invalid dir")
        np.save(fulldir, S)
        np.save(arrfulldir, ori)
        print("saved %s" % filename)
        
        
    def finish(self):
        self.timer.stop()
        self.start.setStyleSheet("background-color: grey")
        print("run finish")

    def aselect_clicked(self):
        self.bselect.setStyleSheet("background-color: grey")
        self.uselect.setStyleSheet("background-color: grey")
        self.aselect.setStyleSheet("background-color: purple")
        self.cur = 'as'

    def bselect_clicked(self):
        self.aselect.setStyleSheet("background-color: grey")
        self.uselect.setStyleSheet("background-color: grey")
        self.bselect.setStyleSheet("background-color: purple")
        self.cur = 'ce'
        
    def uselect_clicked(self):
        self.aselect.setStyleSheet("background-color: grey")
        self.bselect.setStyleSheet("background-color: grey")
        self.uselect.setStyleSheet("background-color: purple")
        self.cur = 'ur'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

