# sample of five layer CNN inference code

"""
Real time prediction with bitscope
"""
from ctypes import *

import time

import librosa
import numpy as np
#import tensorflow as tf
import keras
from cnn5layer import Cnn5layer
import py_bsvml as bv

def print_result(result):
    pred = np.argmax(result,1)
    if pred==0:
        print('prediction : cement')
    else:
        print('predict : asphalt')

SAMPLES = 125000
SAMPLE_RATE = 125000

bsInfo = bv.BitScopeInfo()
bsCount = bv.listBitScopes(1, pointer(bsInfo))

if bsCount == 0:
    exit("Couldn't find a BitScope.")


# load model
model_checkpoint = '/home/junha/makinteract/checkpoint/BitscopeCnn.hdf5'
num_channels = 1
num_rows = 128
num_columns = 245
num_labels = 2 
model = Cnn5layer(num_rows, num_columns, num_channels, num_labels, model_checkpoint)

while(1):
    bs = bv.openBitScope(bsInfo.port)

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
    print("----")
    print(np.max(arr))
    print(np.min(arr))
    print("----")
    arr += np.max(np.abs(data))
    arr /= np.max(np.abs(data))
    #arr /= np.max(data)
    print("----")
    print(np.max(arr))
    print(np.min(arr))
    print("----")
    print(arr[:100])
    S = librosa.feature.melspectrogram(y=arr,sr=SAMPLE_RATE) 
    input_feat = S.reshape(num_channels, num_rows, num_columns, num_channels)
    result = model.predict(input_feat)
    #bias = 0.075
    #result = result + np.array([[bias, -bias]])
    print(result)
    print_result(result)


    time.sleep(2)
