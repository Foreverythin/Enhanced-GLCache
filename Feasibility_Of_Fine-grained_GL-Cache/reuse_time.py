import matplotlib.pyplot as plt
from tqdm import tqdm
import time

# 读取数据
file_path = './wiki2018_partial.txt'  # 请将路径替换为实际文件路径
time_data, id_data, size_data, type_data = [], [], [], []

with open(file_path, 'r') as file:
    for line in file:
        time_, id, size, type = map(int, line.strip().split())
        time_data.append(time_)
        id_data.append(id)
        size_data.append(size)
        type_data.append(type)

# 计算缓存项的重用时间
reuse_times = {}
for i in range(len(id_data)):
    if id_data[i] not in reuse_times:
        reuse_times[id_data[i]] = time_data[i]
    else:
        reuse_times[id_data[i]] = time_data[i] - reuse_times[id_data[i]]

# 设置类型对应的颜色
type_colors = {
    0: 'blue',
    1: 'red',
    2: 'green',
    3: 'yellow',
    4: 'black',
    5: 'pink',
    6: 'purple',
    7: 'orange',
    8: 'gray',
    9: 'brown',
    10: 'cyan',
    11: 'magenta',
    12: 'olive',
    13: 'lime',
    14: 'teal',
    15: 'aqua',
    16: 'indigo',
    17: 'navy',
    18: 'maroon',
}

# 绘制散点图
plt.figure(figsize=(10, 6))
# for i in tqdm(range(len(id_data)), desc='Drawing', ncols=100, ascii=True):
for i in tqdm(range(25000), desc='Drawing', ncols=100, ascii=True):
    time.sleep(0.01)
    try:
        plt.scatter(time_data[i], reuse_times[id_data[i]], color=type_colors[type_data[i]], marker='o')
    except:
        pass
    # plt.scatter(time_data[i], reuse_times[id_data[i]], color=type_colors[type_data[i]], marker='o', s=5, label=f'Type {type_data[i]}')

plt.xticks(range(min(time_data), max(time_data) + 1, 1))


plt.xlabel('Time')
plt.ylabel('Reuse Time')
plt.title('Cache Item Reuse Time')
plt.savefig('./reuse_time.png')
# plt.legend()
# plt.show()
