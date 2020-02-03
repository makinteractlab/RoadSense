import py_bsvml as bv
from ctypes import *

print("DUAL")

bsInfo = bv.BitScopeInfo();
bsCount = bv.listBitScopes(1, pointer(bsInfo))
if bsCount == 0:
    exit("Could not find any BitScopes")

bs = bv.openBitScope(bsInfo.port)
size = 2000

bv.mode(bs, bv.DUAL)
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

bv.trace(bs)
bv.address(bs, bv.getStartAddress(bs))

trace = (c_ubyte * size)()

bv.dumpChannel(bs, bv.CHA)
bv.updateBitScope(bs)
bv.acquire(bs, trace)

# do stuff with channel A data

bv.dumpChannel(bs, bv.CHB)
bv.updateBitScope(bs)
bv.acquire(bs, trace)

# do stuff with channel B data

exit()
