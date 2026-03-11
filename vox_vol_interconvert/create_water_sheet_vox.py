import os

import numpy as np


def generate_phantom(ZThickness_cm):
    VoxX, VoxY, VoxZ = 256, 256, 256
    VoxelSize = 0.125  # cm

    materials = {
        "water": {"id": 2},
        "air": {"id": 1}
    }

    rho_map = {
        1: "0.00120479",  # air
        2: "1.0",  # water
        3: "2.7",  # aluminum（铝的密度大约是2.7 g/cm³）
    }

    ZThickness_vox = int(round(ZThickness_cm / VoxelSize))
    ZThickness_vox = min(ZThickness_vox, VoxZ)

    z_start = (VoxZ - ZThickness_vox) // 2
    z_end = z_start + ZThickness_vox

    # 输出目录
    out_dir = "./data2"
    os.makedirs(out_dir, exist_ok=True)

    for name, mat in materials.items():
        MaterialId = mat["id"]

        print(f"\nGenerating phantom: {name.upper()} slab")

        # ===============================
        # 生成体素
        # ===============================
        vol = np.full((VoxX, VoxY, VoxZ), 1, dtype=np.uint8)
        vol[:, z_start:z_end, :] = MaterialId

        # vol = np.transpose(vol, (2, 1, 0))  # (Y,Z,X)

        # ===============================
        # 保存 raw 文件
        # ===============================
        raw_filename = os.path.join(out_dir, f"Phantom_{name}_{ZThickness_cm}cm.raw")
        vol.tofile(raw_filename)

        # ===============================
        # 保存 mhd 文件
        # ===============================
        mhd_content = (
            f"NDims = 3\n"
            f"DimSize = {VoxX} {VoxY} {VoxZ}\n"
            f"ElementType = MET_UCHAR\n"
            f"ElementSpacing = {VoxelSize} {VoxelSize} {VoxelSize}\n"
            f"ElementDataFile = Phantom_{name}_{ZThickness_cm}cm.raw\n"
        )
        mhd_filename = os.path.join(out_dir, f"Phantom_{name}_{ZThickness_cm}cm.mhd")
        with open(mhd_filename, "w") as fp:
            fp.write(mhd_content)

        # ===============================
        # 保存 vox 文件
        # ===============================
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
        vox_filename = os.path.join(out_dir, f"Phantom_{name}_{ZThickness_cm}cm.vox")
        with open(vox_filename, "w") as fp:
            fp.write(vox_header)
            fp.writelines(vox_lines)

        print(f"Saved: {raw_filename}, {vox_filename}, {mhd_filename}")

    print("\nAll done.")


if __name__ == "__main__":
    # for ZThickness_cm in [1, 2, 4, 6, 8, 12, 16, 20, 30]:
    #     generate_phantom(ZThickness_cm)
    generate_phantom(8)