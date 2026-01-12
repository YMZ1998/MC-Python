import os
import time
import numpy as np
"""
MCGPU .vox 模体生成参考说明
本示例脚本展示了如何用 Python 生成适用于 MCGPU 1.5b 的 .vox 模体文件。
1. 模体基本参数
体素数量：VoxSizeX, VoxSizeY, VoxSizeZ
体素物理尺寸：VoxelSizeX, VoxelSizeY, VoxelSizeZ（单位 cm）
→ 二者决定了整体模体的几何大小。
2. 材料定义
每种材料需指定：
ID（整数，唯一标识）
质量密度（g/cm³）
示例：空气、PMMA、铁。
可根据需要添加或修改材料

3. 体素赋值
默认初始化为某种背景材料（如空气）。
通过数组索引设置特定区域为指定材料：
整块区域（如 PMMA 板）
局部块/嵌入物（如金属小体）
→ 用户可自行修改位置、厚度和材料。

4. 文件输出结构
生成的 .vox 文件包括：
头部信息：体素数量、体素尺寸、列定义。
逐体素数据：
<MATERIAL_ID> <DENSITY>
文件写入后可直接作为 MCGPU 输入模体。

下面代码生成：
10cm*10cm的小体积模体，并将附加材料放置一个 fe 附加物

⚠️注意！！！XYZ的方向可能不满足你的需求，需要根据投影方向调整
"""
VoxSizeX = 20
VoxSizeZ = 20

# 体素物理尺寸（单位 cm）
VoxelSizeX = 0.5
VoxelSizeZ = 0.5
VoxelSizeY = 0.1


thickness_fe = 1


# 定义材料密度
density_air = 0.00120479  # 空气
density_pmma = 1.18  # PMMA
density_fe = 7.874  # 铁


# 定义材料 ID
AirID = 1
PMMAID = 2
FeID = 3

# 输出文件夹
output_dir = "./vox_file"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def mainFunction(thickness_pmma):
    VoxSizeY = thickness_pmma + 50  # 以最大厚度为基准
    # 初始化体素空间
    mat_id = np.ones((VoxSizeX, VoxSizeY, VoxSizeZ), dtype=int) * AirID
    length_half = 1  # 2*0.5 = 2cm
    pmma_start_y = 50
    pmma_end_y = 50 + thickness_pmma
    # 设置Fe区域
    fe_x = 12
    fe_z = 15
    for y in range(0, thickness_fe):
        for x in range(fe_x - length_half, fe_x + length_half):
            for z in range(fe_z - length_half, fe_z + length_half):
                mat_id[x, y, z] = FeID

    # 设置PMMA区域,整个纵截面
    mat_id[:, pmma_start_y:pmma_end_y, :] = PMMAID

    # 生成 .vox 文件
    #    - 文件头：维度 & 体素尺寸 & 列信息
    #    - 每体素：材料ID & 对应材料的密度
    # -------------------------------------------------
    # 使用列表代替字符串拼接提高性能(空间换时间)
    vox_lines = []
    vox_lines.append("[SECTION VOXELS phantomER]\n")
    vox_lines.append(f"{VoxSizeX} {VoxSizeY} {VoxSizeZ} No. OF VOXELS IN X,Y,Z\n")
    vox_lines.append(f"{VoxelSizeX} {VoxelSizeY} {VoxelSizeZ} VOXEL SIZE(cm) ALONG X, Y, Z\n")
    vox_lines.append("1 COLUMN NUMBER WHERE MATERIAL ID IS LOCATED\n")
    vox_lines.append("2 COLUMN NUMBER WHERE THE MASS DENSITY IS LOCATED\n")
    vox_lines.append("0 BLANK LINES AT END OF X,Y-CYCLES (1=YES,0=NO)\n")
    vox_lines.append("[END OF VXH SECTION]\n")

    # 定义材料密度数组 Rhos
    Rhos = [
        None,  # 占位 (ID=0 不用)
        str(density_air),  # ID=1 => 空气
        str(density_pmma),  # ID=2 => PMMA

        str(density_fe),  # ID=3 => 铁
    ]

    # 预转换数据为列表
    print(f"P{thickness_pmma}mm_MutipleMaterialsBot.vox start to write")

    # 记录开始时间
    start_time = time.time()
    mat_id_flat = mat_id.flatten()
    data_lines = []
    for mid in mat_id_flat:
        data_lines.append(f"{mid} {Rhos[mid]}\n")  # 直接追加格式化字符串

    # 合并所有行（比字符串拼接快约5-10倍）
    vox_lines += data_lines

    # 写入文件
    vox_filename = f"{output_dir}/P{thickness_pmma}mm_MutipleMaterialsBot_mini.vox"
    with open(vox_filename, 'w') as fp:
        fp.writelines(vox_lines)  # 使用writelines直接写入列表

    # 记录结束时间
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Done writing {vox_filename}.")
    print(f"Execution time: {execution_time} seconds\n--------\n")

for pmma_thickness in range(20, 21, 10):
    mainFunction(pmma_thickness)