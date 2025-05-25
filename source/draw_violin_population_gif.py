#做GIF
import imageio
import os

# 圖片路徑
img_dir = "../picture/"
# 收集所有圖檔（排序很重要）
file_list = sorted(
    [f for f in os.listdir(img_dir) if f.startswith("population_by_4_age_sex_violin_") and f.endswith(".png")]
)

# 生成 GIF
images = []
for filename in file_list:
    path = os.path.join(img_dir, filename)
    images.append(imageio.v2.imread(path))

# 儲存
imageio.mimsave(img_dir+"population_violin_animation.gif", images, fps=6, loop=0)  # fps: 每秒幾張圖