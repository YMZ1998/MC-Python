import os

import numpy as np

# 加载 .npy 文件
data_path = "./vox_vol_interconvert"
name = "WaterPhantom.npy"
phantom = np.load(os.path.join(data_path, name))

# 获取 shape 和 dtype
shape_str = "x".join(map(str, phantom.shape))  # 例如 512x512x70
dtype_str = str(phantom.dtype)  # 例如 float32
print(shape_str, dtype_str)

# 构建带信息的 raw 文件名
raw_file = os.path.join(
    data_path,
    name.replace(".raw", f"_{shape_str}_{dtype_str}.raw")
)

# 保存为 .raw
phantom.tofile(raw_file)

print(f"已保存为 {raw_file}")
