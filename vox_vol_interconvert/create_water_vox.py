# Generate water plate phantom .vox

import numpy as np

# The whole volume.

VoxX = 256
VoxY = 256
VoxZ = 256
VoxelSize = 0.125  # cm
WaterMaterialId = 2  # Material index in .in file

for WaterThickness in range(11, 21):  # cm
    # The water plate.
    ModelX = 128  # 4cm
    ModelY = int(WaterThickness / VoxelSize)
    ModelZ = 128
    vol = np.ones((VoxX, VoxY, VoxZ), dtype=int)
    xl = (VoxX - ModelX) // 2
    yl = (VoxY - ModelY) // 2
    zl = (VoxZ - ModelZ) // 2

    vol[xl:xl + ModelX, yl:yl + ModelY, zl:zl + ModelZ] = WaterMaterialId

    voxFile = ""
    voxFile += "[SECTION VOXELS phantomER]\n{} {} {} No. OF VOXELS IN X,Y,Z\n{} {} {} VOXEL SIZE (cm) ALONG X,Y,Z\n".format(
        VoxX, VoxY, VoxZ, VoxelSize, VoxelSize, VoxelSize)
    voxFile += "1 COLUMN NUMBER WHERE MATERIAL ID IS LOCATED\n"
    voxFile += "2 COLUMN NUMBER WHERE THE MASS DENSITY IS LOCATED\n"
    voxFile += "0 BLANK LINES AT END OF X,Y-CYCLES (1=YES,0=NO)\n"
    voxFile += "[END OF VXH SECTION]\n"

    Rhos = [None, '0.00120479', '1']  # Density

    vol = vol.flatten()
    # Save corresponding .raw volume.
    # Use ImageJ Volume Viewer to display.
    # Ray points to +y in ImageJ coordinate when "0.0 1.0 0.0  # SOURCE DIRECTION COSINES: U V W"
    with open('WaterPhantom.raw', 'wb') as fp:
        fp.write(vol.astype(np.uint8).tobytes())

    # Generate .vox file.
    for i in range(vol.shape[0]):
        voxFile += "{} {}\n".format(str(vol[i]), Rhos[vol[i]])

    SavePath = str(WaterThickness) + 'cm.vox'
    with open(SavePath, 'w') as fp:
        fp.write(voxFile)

    print('Done {} cm.'.format(WaterThickness))
