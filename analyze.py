import output
import objloader
import numpy


aa = objloader.Obj.open('./3dobj/lite.obj')

data = aa.to_array()
print(data)

