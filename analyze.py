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

##import numpy

infile_name = input("输入读取文件路径:")
outfile_name = input("输入导出文件名：***.schem:\n")
if outfile_name == "":
    outfile_name == "out"

print("正在分析OBJ...")
Object = objloadN.OBJN(infile_name)
data = Object.Exp_V()

print("正在导出文件：", outfile_name + ".schem")
out = output.SchemN(data)
out.Exp_sch(outfile_name)
