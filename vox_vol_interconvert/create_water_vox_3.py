import numpy as np

VoxX, VoxY, VoxZ = 256, 256, 256
VoxelSize = 0.1  # cm
ZThickness_cm = 8

materials = {
    "water": {"id": 2},
    "air": {"id": 1}
}

rho_map = {
    1: "0.00120479",  # air
    2: "1.0",  # water
}

ZThickness_vox = int(round(ZThickness_cm / VoxelSize))
ZThickness_vox = min(ZThickness_vox, VoxZ)

z_start = (VoxZ - ZThickness_vox) // 2
z_end = z_start + ZThickness_vox

for name, mat in materials.items():
    MaterialId = mat["id"]

    print(f"\nGenerating phantom: {name.upper()} slab")

    # 外围空气
    vol = np.full((VoxX, VoxY, VoxZ), 1, dtype=np.uint8)
    vol[z_start:z_end, :, :] = MaterialId

    # raw
    raw_filename = f"Phantom_{name}_{ZThickness_cm}cm.raw"
    vol.tofile(raw_filename)

    # vox
    vox_header = (
        f"[SECTION VOXELS phantomER]\n"
        f"{VoxX} {VoxY} {VoxZ} No. OF VOXELS IN X,Y,Z\n"
        f"{VoxelSize} {VoxelSize} {VoxelSize} VOXEL SIZE (cm) ALONG X,Y,Z\n"
        f"1 COLUMN NUMBER WHERE MATERIAL ID IS LOCATED\n"
        f"2 COLUMN NUMBER WHERE THE MASS DENSITY IS LOCATED\n"
        f"0 BLANK LINES AT END OF X,Y-CYCLES (1=YES,0=NO)\n"
        f"[END OF VXH SECTION]\n"
    )

    vol_flat = vol.flatten(order="F")
    vox_lines = [f"{v} {rho_map[v]}\n" for v in vol_flat]

    vox_filename = f"Phantom_{name}_{ZThickness_cm}cm.vox"
    with open(vox_filename, "w") as fp:
        fp.write(vox_header)
        fp.writelines(vox_lines)

    print(f"Saved: {raw_filename}, {vox_filename}")

print("\nDone.")
