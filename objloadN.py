"""
Load and pack *.obj files
加载和打包.obj文件数据
---
#不支持:
四点面
O(分组)
S

IDLE:VS CODE
Python Version:3.11.5/3.10.11/
@PuiChing Memory
"""

import re
from rich.progress import track
import rich.progress
import os
import math

# import PIL.Image
from PIL import Image


class mtlN:
	"""
	mtl文件对象
	---
	"""

	def __init__(self, *path) -> None:
		self._enc_data = []  # 解析mtl行列表
		self.child = []  # mtl子对象
		self.path = path
		if path != ():
			self.open(path)

	def open(self, path):
		self.path = path
		print("load mtl file from:", path)
		with open(path) as data:
			# 过滤无关字符
			for i in data.readlines():
				i.replace("\n", "")
				if i[0] == "#":
					continue
				if i == "\n":
					continue
				self._enc_data.append(i.replace("\n", ""))
		#print(self._enc_data)

		self._analyze()

	def _analyze(self):
		current = 0
		for i in self._enc_data:
			if str(i).startswith("newmtl"):
				self.child.append(mtlC(i[7:]))
				current = len(self.child) - 1
				continue

			if str(i).startswith("Ns"):
				self.child[current].set_ns(float(i[3:]))
				continue

			if str(i).startswith("Ni"):
				self.child[current].set_ni(float(i[3:]))
				continue
				
			if str(i).startswith("d"):
				self.child[current].set_d(float(i[2:]))
				continue
			
			if str(i).startswith("illum"):
				self.child[current].set_illum(int(i[6:]))
				continue

			if str(i).startswith("Ka"):
				temp = i[3:].split(" ")
				temp_ka = [float(x) for x in temp]
				self.child[current].set_ka(temp_ka)
				continue

			if str(i).startswith("Ks"):
				temp = i[3:].split(" ")
				temp_ks = [float(x) for x in temp]
				self.child[current].set_ks(temp_ks)
				continue

			if str(i).startswith("Ke"):
				temp = i[3:].split(" ")
				temp_ke = [float(x) for x in temp]
				self.child[current].set_ke(temp_ke)
				continue
				
			if str(i).startswith("Kd"):
				temp = i[3:].split(" ")
				temp_ke = [float(x) for x in temp]
				self.child[current].set_kd(temp_ke)
				continue
			
			if str(i).startswith('map_Kd'):
				self.child[current].set_map_kd(os.path.dirname(self.path) + '/' + i[7:])
				continue


		#print(self.child[0].get())

	def get_pixel(self,img_index:int,x_scale:float,y_scale:float):
		#print(img_index)
		x_scale = math.modf(x_scale)[0]
		y_scale = math.modf(y_scale)[0]

		data = self.child[img_index].get_colour(self.child[img_index].get_map_size()[0] * x_scale,self.child[img_index].get_map_size()[1] * y_scale)
		return data


class mtlC:
	"""
	mtl子对象
	---
	"""

	def __init__(self, id) -> None:
		self.id = id
		self.ka = []
		self.kd = []
		self.ks = []
		self.ke = []
		self.d = 0.0
		self.ns = 0.0
		self.ni = 0.0
		self.illum = 0
		self.map_Kd = ""
		self.map_x = 0
		self.map_y = 0
		self.map_obj = object

	def set_ns(self, ns: float):
		# print(ns)
		self.ns = ns

	def set_ka(self, ka: list):
		# print(ka)
		self.ka = ka

	def set_ks(self, ks: list):
		# print(ks)
		self.ks = ks

	def set_ke(self, ke: list):
		# print(ke)
		self.ke = ke
		
	def set_kd(self, kd: list):
		# print(ke)
		self.kd = kd

	def set_ni(self, ni: float):
		# print(ni)
		self.ni = ni

	def set_d(self, d: float):
		self.d = d

	def set_illum(self, illum: int):
		self.illum = illum

	def set_map_kd(self, map_kd: str):
		self.map_Kd = os.path.abspath(map_kd)
		self.map_obj = Image.open(self.map_Kd)
		self.map_x = self.map_obj.width
		self.map_y = self.map_obj.height

	def get_id(self) -> str:
		return self.id

	def get_map_Kd(self) -> str:
		return self.map_Kd

	def get(self) -> list:
		return [
			self.id,
			self.ka,
			self.kd,
			self.ke,
			self.ks,
			self.d,
			self.ns,
			self.ni,
			self.illum,
			self.map_Kd,
			self.map_x,
			self.map_y,
			self.map_obj,
		]
	def get_map_size(self):
		return (self.map_x,self.map_y)
	
	def get_colour(self, x, y) -> list:
		#print('x',x,'y',y)
		return self.map_obj.getpixel((round(x,0)-1,round(y,0)-1))


class OBJN:
	"""
	OBJ文件对象
	---
	从文件加载:__init__ or open() \n
	导出数据:Exp_V()
	"""

	def __init__(self, *path: str) -> "OBJN":
		self._enc_data = []

		if path != ():
			self.Open(path[0])

	def Open(self, path: str):
		self.path = path
		self._enc_data = []
		with rich.progress.open(path, encoding="utf-8") as file:
			# 过滤无关字符
			for i in file.readlines():
				if i[0] == "#":
					continue
				if i == "\n":
					continue

				self._enc_data.append(i)

	def Exp_V(self) -> list:
		"""
		导出数据
		---
		list[0] = v_list #顶点列表\n
		list[1] = vn_list #法向量列表\n
		list[2] = vt_list #uv列表\n
		list[3] = f_list #面列表\n
		list[4] = mtllib #mtl文件对象\n
		list[5] = strc #f分组结构
		"""
		if self._enc_data == []:
			raise IndexError("导出错误:数据未载入,先调用Open(path)")

		_exp_v = []
		_exp_vn = []
		_exp_f = []
		_exp_vt = []
		_exp_mtllib = mtlN()
		_exp_strc = []

		for i in track(self._enc_data, description="分析点v数据"):
			# 使用正则表达式提取以"v"开头的行
			vertices = re.findall(r"v\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)", i)

			# 遍历提取到的顶点数据
			for vertex in vertices:
				x, y, z = vertex  # 将每行的数据分为三份
				_exp_v.append([float(x), float(y), float(z)])

		for i in track(self._enc_data, description="分析法向量vn数据"):
			# 使用正则表达式提取以"vn"开头的行
			vertices = re.findall(r"vn\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)", i)

			# 遍历提取到的顶点数据
			for vertex in vertices:
				x, y, z = vertex  # 将每行的数据分为三份
				_exp_vn.append([float(x), float(y), float(z)])

		# print(_exp_vn)
		for i in track(self._enc_data, description="分析(uv)vt数据"):
			# 使用正则表达式提取 vt 行，并将它们转换为 [x, y] 的列表形式
			matches = re.findall(r"vt (\d+\.\d+)\s(\d+\.\d+)", i)
			for match in matches:
				x, y = match
				_exp_vt.append([float(x), float(y)])

		for i in track(self._enc_data, description="分析面f数据"):
			# 使用正则表达式提取以"f"开头的行
			# matches = re.findall( r"f (\d+/\d+/\d+ \d+/\d+/\d+ \d+/\d+/\d+ \d+/\d+/\d+)" , i, re.MULTILINE)
			matches = re.findall(
				r"f (\d+/\d+/\d+ \d+/\d+/\d+ \d+/\d+/\d+)", i, re.MULTILINE
			)
			# 将找到的匹配项保存到列表中

			for match in matches:
				int_list = [
					[int(i) for i in match.split(" ")[i].split("/")]
					for i in range(len(match.split(" ")))
				]
				_exp_f.append(int_list)

		for i in track(self._enc_data, description="解析mtl"):
			if i.startswith("mtllib") == True:
				try:
					_exp_mtllib.open(os.path.dirname(self.path) + "/" + i[7:-1])
				except Exception as error:
					print(error)

		strc_count = 0
		#_exp_strc.append('D')
		for i in track(self._enc_data, description="分析usemtl结构"):
			if str(i).startswith('f'):
				strc_count = strc_count + 1
				continue
			
			if str(i).startswith('usemtl'):
				_exp_strc.append(strc_count)
				#_exp_strc.append('M')
				strc_count = 0
		_exp_strc.append(strc_count)

		return [_exp_v, _exp_vn, _exp_vt, _exp_f, _exp_mtllib,_exp_strc]


if __name__ == "__main__":
	Object = OBJN()
	Object.Open("3dobj/tex/tex.obj")
	#Object.Open("2E.obj")
	result = Object.Exp_V()
	print(result[5])
