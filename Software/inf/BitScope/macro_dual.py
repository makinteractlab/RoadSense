import py_bsvml as bv
from ctypes import *
import time

print("DUAL MACRO")

bsInfo = bv.BitScopeInfo()
bsCount = bv.listBitScopes(1, pointer(bsInfo))

if bsCount == 0:
    exit("Couldn't find a BitScope.\n")

bs = bv.openBitScope(bsInfo.port)
size = 2000

bv.mode(bs, bv.DUAL)
bv.macro(bs, True)
bv.rate(bs, 1000000)
bv.traceIntro(bs, 1)
bv.traceOutro(bs, size)
bv.traceDelay(bs, 0) # ms
bv.traceTimeout(bs, bv.getMinTimeout(bs)) # ms
bv.trigType(bs, bv.COMP)
bv.trigIntro(bs, 4) # samples
bv.trigOutro(bs, 4) # samples
bv.trigLevel(bs, 2) # v
bv.range(bs, 8.0) # v
bv.offset(bs, 0.0) # v
bv.dumpSize(bs, size)
bv.updateBitScope(bs)

byteCount = bv.getBytesInDump(bs)
rawData = (c_ubyte * byteCount)()
macroTrace = (c_short * size)()

bv.trace(bs)
bv.address(bs, bv.getStartAddress(bs)) # update AFTER tracing

# get data for channel A
bv.dumpChannel(bs, bv.CHA)
bv.updateBitScope(bs) # updates for preceeding call to `bv.address` aswell
bv.acquire(bs, rawData)

# convert it from raw bytes to shorts
bv.convertMacroTrace(rawData, macroTrace, byteCount)

# do stuff with channel A trace

# now for channel B
bv.dumpChannel(bs, bv.CHB)
bv.updateBitScope(bs)
bv.acquire(bs, rawData)

# convert into 16 bits
bv.convertMacroTrace(rawData, macroTrace, byteCount)

# do stuff with channel B trace

exit()
