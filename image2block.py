from PIL import Image
import mcschematic

import time


mc_block = {
    "minecraft:white_concrete": (205, 210, 211),
    "minecraft:light_gray_concrete": (124, 124, 114),
    "minecraft:gray_concrete": (53, 56, 60),
    "minecraft:black_concrete": (8, 10, 15),
    "minecraft:brown_concrete": (96, 59, 32),
    "minecraft:red_concrete": (141, 33, 33),
    "minecraft:orange_concrete": (222, 96, 0),
    "minecraft:yellow_concrete": (238, 173, 21),
    "minecraft:lime_concrete": (94, 168, 25),
    "minecraft:green_concrete": (72, 90, 36),
    "minecraft:cyan_concrete": (21, 117, 133),
    "minecraft:light_blue_concrete": (35, 134, 195),
    "minecraft:blue_concrete": (44, 46, 142),
    "minecraft:purple_concrete": (99, 31, 154),
    "minecraft:magenta_concrete": (165, 46, 155),
    "minecraft:pink_concrete": (210, 99, 140),
}


##print(mc_block["minecraft:white_concrete"])


def get_pixel_values(image_path: str, filename: str):
    # 打开图片
    img = Image.open(image_path)

    # 获取图片的尺寸
    width, height = img.size
    print(width,height)
    schem = mcschematic.MCSchematic()
    print('分析中')
    # 循环遍历每个像素点
    for x in range(width):
        for y in range(height):
            ##time.sleep(0.1)
            # 获取当前像素点的RGB值
            rgba = img.getpixel((x, y))
            # 打印RGB值
            ##print(rgba)
            rsumm = 999
            tar_block = ""
            for i in mc_block.keys():
                # mc_block[i]
                summ = 0
                for c1, c2 in zip(rgba, mc_block[i]):
                    summ = summ + abs(c1 - c2)

                if summ < rsumm:
                    rsumm = summ
                    tar_block = i

            ##print(tar_block)

            schem.setBlock((x, 0, y), tar_block)

    print('保存数据。。。')
    schem.save(  "./", filename, mcschematic.Version.JE_1_20_1)


path = input("图片路径：")

# 使用图片路径调用函数

get_pixel_values(path, "out")
