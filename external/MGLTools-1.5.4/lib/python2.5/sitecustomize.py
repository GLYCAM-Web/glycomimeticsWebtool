mglroot = '/programs/glycomimeticsWebtool/external/MGLTools-1.5.4'
# specify mglroot here
import sys, os
path = os.path.join(mglroot, "MGLToolsPckgs")
sys.path.insert(0,path)

from Support.path import setSysPath
setSysPath(path)
#sys.path.insert(0,'.')