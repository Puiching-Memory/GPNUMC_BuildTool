"""
analyize the file of .obj
分析.obj文件
---
IDLE:VS CODE
Python Version:3.11.5
@PuiChing Memory
"""


import output
import objloadN
import numpy

Object = objloadN.OBJN("./3dobj/3F.obj")
data = Object.Exp_V()

out = output.SchemN(data)
out.Exp_sch()