


TYPE = 4

# 读取数据
file_path = './wiki2018_100000.txt' 

target_file_path = './wiki2018_100000_type_' + str(TYPE) + '.txt'



f = open(target_file_path, 'w')

with open(file_path, 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        time_, id, size, type = map(int, line.strip().split())
        if type == TYPE:
            f.write(line)
    
f.close()
