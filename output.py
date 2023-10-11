"""
导出为.schem文件
---
IDLE:VS CODE
Python Version:3.11.5
@PuiChing Memory
"""


import mcschematic

class SchemN():
    def __init__(self,data:list) -> None:
        self.data = data

    def Exp_sch(self):
        schem = mcschematic.MCSchematic()
        for i in self.data:
            schem.setBlock(  (int(i[0]), int(i[2]), int(i[1])), "minecraft:stone"  )

        schem.save(  "./", "test", mcschematic.Version.JE_1_20_1)





