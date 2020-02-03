import sys
import time
from ctypes import *

import librosa
import numpy as np
import keras

from cnn8layer import Cnn8layer
import py_bsvml as bv

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, QSizePolicy, QHBoxLayout,     QVBoxLayout, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer, QRect, QThread
from PyQt5.QtGui import *

# blue : asphalt
# yellow : bike
# green : block

def print_result(result):
    pred = np.argmax(result,1)
    if pred==0:
        print('prediction : block')
        return 'block'
    elif pred == 1:
        print('predict : asphalt')
        return 'asphalt'
    else:
        print('predict : bike')
        return 'bike'

class WorkThread(QThread):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.state = 'asphalt'

    def __del__(self):
        self.wait()

    def run(self):

        SAMPLES = 10000
        SAMPLE_RATE = 10000

        bsInfo = bv.BitScopeInfo()
        bsCount = bv.listBitScopes(1, pointer(bsInfo))
        bs = bv.openBitScope(bsInfo.port)

        if bsCount == 0:
            exit("Couldn't find a BitScope.")

        # load model
        model_checkpoint = 'C:/Users/MAKinteract/makinteract/checkpoint/8layer_tri_v2_0131.hdf5'
        num_channels = 1
        num_rows = 128
        num_columns = 20
        num_labels = 3
        model = Cnn8layer(num_rows, num_columns, num_channels, num_labels, model_checkpoint)

        while(1):
            #bs = bv.openBitScope(bsInfo.port)
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

            #print("acquired %d data" % len(data))
            arr = np.array(data,dtype=np.float64)
            ori = arr
            div = (np.max(arr)-np.min(arr))/2.
            if div==0:
                div = 1.
            arr = arr / div
            arr = arr - arr.mean(axis=0)
            S = librosa.feature.melspectrogram(y=arr,sr=SAMPLE_RATE)
            input_feat = S.reshape(num_channels, num_rows, num_columns, num_channels)
            result = model.predict(input_feat)
            #bias = 0.075
            #result = result + np.array([[bias, -bias]])
            print("********************")
            print(result)
            self.state = print_result(result)
            print("********************")
            
            self.sig.emit(self.state)
            time.sleep(0.1)

            
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Hyundai project Demo'
        self.left = 10
        self.top = 10
        self.width = 1320
        self.height = 1200

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: blue")

        self.label = QLabel('asphalt',self) 
        self.label.setStyleSheet("font: 80pt Comic Sans MS")
        self.label.setGeometry(QRect(0, 0, 1320, 1200))
        self.label.move(530,-250)

        work = WorkThread()
        work.sig.connect(self.change_color)
        work.start()

        self.show()

    def change_color(self, state):
        if  state == 'asphalt':
            self.setStyleSheet("background-color: blue")
            self.label.setText("asphalt")
        elif state == 'block':
            self.setStyleSheet("background-color: red")
            self.label.setText("block")
        elif state  == 'bike':
            self.setStyleSheet("background-color: yellow")
            self.label.setText("bike")
        else:
            self.setStyleSheet("background-color: grey")



        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


