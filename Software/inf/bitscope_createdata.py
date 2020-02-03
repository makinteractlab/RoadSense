"""
Create spectrogram data with bitscope
"""
from ctypes import *

import os
import time
from os.path import join

import librosa

import numpy as np
#import tensorflow as tf
#import keras
#from cnn5layer import Cnn5layer
import py_bsvml as bv
from sklearn.preprocessing import normalize

TASK = input("Task (a or b): ")
iteration = input("file indicator: ") 

DATA_FOLDER = 'C:/Users/MAKinteract/makinteract'
as_dir = join(DATA_FOLDER, 'as')
ce_dir = join(DATA_FOLDER, 'ce')
if not os.path.exists(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)
if not os.path.exists(as_dir):
    os.mkdir(as_dir)
if not os.path.exists(ce_dir):
    os.mkdir(ce_dir)

SAMPLES = 10000
SAMPLE_RATE = 10000

bsInfo = bv.BitScopeInfo()
bsCount = bv.listBitScopes(1, pointer(bsInfo))

if bsCount == 0:
    exit("Couldn't find a BitScope.")
bs = bv.openBitScope(bsInfo.port)

# load model


    
    
def record():
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

    print("acquired %d data" % len(data))
    arr = np.array(data,dtype=np.float64)
    print("before max: ",np.max(arr))
    print("before min: ",np.min(arr))
    
    #arr = arr - arr.mean(axis=0)
    """
    div = np.abs(arr).max(axis=0)
    if div == 0:
        div = 1.
    arr = arr / div
    """
    """
    for j in range(len(arr)):
        print(arr[j])
    """
    #arr = normalize(arr[:,np.newaxis],axis=0).ravel()
    #arr /= np.max(data)
    print("----")
    print(np.max(arr))
    print(np.min(arr))
    print("----")
    S = librosa.feature.melspectrogram(y=arr,sr=SAMPLE_RATE)
    filename = TASK+ '_' + str(iteration)+'_'+str(i+1)
    if TASK == 'a':
        fulldir = join(as_dir, filename)
    elif TASK == 'b':
        fulldir = join(ce_dir, filename)
    else:
        print("invalid dir")
    np.save(fulldir, S)
    print("saved %s" % filename)

for i in range(3):
    record()
    
print("done")

