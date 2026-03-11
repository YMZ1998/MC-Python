import numpy as np

# ===============================
# 基本参数
# ===============================
VoxX, VoxY, VoxZ = 256, 256, 256
VoxelSize_cm = 0.1
VoxelSize_mm = VoxelSize_cm * 10.0

ZThickness_cm = 8.0
Gap_cm = 1.0

# 材质 ID
AIR = 1
WATER = 2

rho_map = {
    AIR: "0.00120479",
    WATER: "1.0",
}

# ===============================
# Z 方向厚度
# ===============================
ZThickness_vox = int(round(ZThickness_cm / VoxelSize_cm))
ZThickness_vox = min(ZThickness_vox, VoxZ)

z_start = (VoxZ - ZThickness_vox) // 2
z_end = z_start + ZThickness_vox

# ===============================
# 圆柱半径（留 gap）
# ===============================
MaxRadius_cm = min(VoxX, VoxY) * VoxelSize_cm / 2
Radius_cm = MaxRadius_cm - Gap_cm
Radius_vox = int(round(Radius_cm / VoxelSize_cm))

print(f"Cylinder radius = {Radius_cm:.2f} cm")
print(f"Gap = {Gap_cm:.2f} cm")

# ===============================
# XY 网格
# ===============================
cx = VoxX // 2
cy = VoxY // 2

yy, xx = np.meshgrid(
    np.arange(VoxY),
    np.arange(VoxX)
)

r2 = (xx - cx) ** 2 + (yy - cy) ** 2
mask_xy = r2 <= Radius_vox ** 2

# ===============================
# 生成体数据
# ===============================
print("\nGenerating water cylinder phantom...")

vol = np.full((VoxX, VoxY, VoxZ), AIR, dtype=np.uint8)

for z in range(z_start, z_end):
    vol[:, :, z][mask_xy] = WATER

# ===============================
# 保存 RAW（C-order）
# ===============================
raw_filename = "Phantom_water_Cylinder_8cm.raw"
vol.tofile(raw_filename)

# ===============================
# 保存 MHD
# ===============================
mhd_filename = "Phantom_water_Cylinder_8cm.mhd"

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
# 保存 VOX（phantomER 格式）
# ===============================
vox_filename = "Phantom_water_Cylinder_8cm.vox"

vox_header = (
    f"[SECTION VOXELS phantomER]\n"
    f"{VoxX} {VoxY} {VoxZ} No. OF VOXELS IN X,Y,Z\n"
    f"{VoxelSize_cm} {VoxelSize_cm} {VoxelSize_cm} VOXEL SIZE (cm) ALONG X,Y,Z\n"
    f"1 COLUMN NUMBER WHERE MATERIAL ID IS LOCATED\n"
    f"2 COLUMN NUMBER WHERE THE MASS DENSITY IS LOCATED\n"
    f"0 BLANK LINES AT END OF X,Y-CYCLES (1=YES,0=NO)\n"
    f"[END OF VXH SECTION]\n"
)

# phantomER / EGSnrc 一般要求 Fortran order
vol_flat_F = vol.flatten(order="F")
vox_lines = [f"{v} {rho_map[v]}\n" for v in vol_flat_F]

with open(vox_filename, "w") as f:
    f.write(vox_header)
    f.writelines(vox_lines)

# ===============================
# 完成
# ===============================
print(f"Saved: {raw_filename}")
print(f"Saved: {mhd_filename}")
print(f"Saved: {vox_filename}")
print("\nDone.")
