import numpy as np

# ===============================
# 基本参数
# ===============================
VoxX, VoxY, VoxZ = 256, 256, 256
VoxelSize_cm = 0.1
VoxelSize_mm = VoxelSize_cm * 10.0

AIR = 1
WATER = 2

rho_map = {
    AIR: "0.00120479",
    WATER: "1.0",
}

# ===============================
# X 方向水柱长度
# ===============================
XThickness_cm = 8.0
XThickness_vox = int(round(XThickness_cm / VoxelSize_cm))
x_start = (VoxX - XThickness_vox) // 2
x_end = x_start + XThickness_vox

# ===============================
# 圆柱半径（YZ 面）
# ===============================
Gap_cm = 1.0
Radius_cm = min(VoxY, VoxZ) * VoxelSize_cm / 2 - Gap_cm
Radius_vox = int(Radius_cm / VoxelSize_cm)

# ===============================
# 坐标（X,Y,Z 顺序）
# ===============================
xx, yy, zz = np.meshgrid(
    np.arange(VoxX),
    np.arange(VoxY),
    np.arange(VoxZ),
    indexing="ij"
)

cy, cz = VoxY // 2, VoxZ // 2

# ===============================
# 初始化
# ===============================
vol = np.full((VoxX, VoxY, VoxZ), AIR, dtype=np.uint8)

# ===============================
# 水圆柱（轴向 X）
# ===============================
mask_cylinder = (
                    (yy - cy) ** 2 + (zz - cz) ** 2 <= Radius_vox ** 2
                ) & (xx >= x_start) & (xx < x_end)

vol[mask_cylinder] = WATER

# ===============================
# X 轴同轴贯通孔（YZ 面圆）
# ===============================
hole_radius = 12 * (0.1 / VoxelSize_cm)
offset = Radius_vox - hole_radius - 20* (0.1 / VoxelSize_cm)

hole_centers = [
    (cy, cz - offset),  # 上
    (cy + offset, cz),  # 右
    (cy, cz),
    (cy, cz + offset),  # 下
    (cy - offset, cz),  # 左
]

for y0, z0 in hole_centers:
    hole_mask = (yy - y0) ** 2 + (zz - z0) ** 2 <= hole_radius ** 2
    vol[hole_mask & mask_cylinder] = AIR

vol = np.transpose(vol, (1, 2, 0))  # (Y,Z,X)
# ===============================
# 保存 RAW
# ===============================
raw_filename = "Phantom_WaterCylinder_XAxis.raw"
vol.tofile(raw_filename)

# ===============================
# 保存 MHD
# ===============================
mhd_filename = "Phantom_WaterCylinder_XAxis.mhd"
mhd_content = f"""ObjectType = Image
NDims = 3
BinaryData = True
BinaryDataByteOrderMSB = False
CompressedData = False
TransformMatrix = 1 0 0  0 1 0  0 0 1
Offset = 0 0 0
CenterOfRotation = 0 0 0
ElementSpacing = {VoxelSize_mm} {VoxelSize_mm} {VoxelSize_mm}
DimSize = {VoxX} {VoxY} {VoxZ}
ElementType = MET_UCHAR
ElementDataFile = {raw_filename}
"""
with open(mhd_filename, "w") as f:
    f.write(mhd_content)

# ===============================
# 保存 VOX（phantomER）
# ===============================
vox_filename = "Phantom_WaterCylinder_XAxis.vox"

vox_header = (
    "[SECTION VOXELS phantomER]\n"
    f"{VoxX} {VoxY} {VoxZ} No. OF VOXELS IN X,Y,Z\n"
    f"{VoxelSize_cm} {VoxelSize_cm} {VoxelSize_cm} VOXEL SIZE (cm) ALONG X,Y,Z\n"
    "1 COLUMN NUMBER WHERE MATERIAL ID IS LOCATED\n"
    "2 COLUMN NUMBER WHERE THE MASS DENSITY IS LOCATED\n"
    "0 BLANK LINES AT END OF X,Y-CYCLES (1=YES,0=NO)\n"
    "[END OF VXH SECTION]\n"
)

# phantomER 要求 X 最快
vol_F = vol.flatten(order="F")

with open(vox_filename, "w") as f:
    f.write(vox_header)
    for v in vol_F:
        f.write(f"{v} {rho_map[v]}\n")

# ===============================
# 完成
# ===============================
print("✔ 圆柱轴向：X")
print("✔ 插件孔轴向：X（同轴）")
print("✔ 4 个方向区分孔")
print("✔ RAW / MHD / VOX 已生成")
