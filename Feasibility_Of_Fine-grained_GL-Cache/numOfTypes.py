from tqdm import tqdm
import time

file_path = '../data/eag_300m.csv'

output_file_path = './eag_300m_types_num.txt'

num_lines = 300000000

num_dict = dict()

with open(file_path, 'r') as file:
    types = set()
    line = file.readline()
    for i in tqdm(range(num_lines)):
        # time.sleep(0.00000000000000001)
        line = file.readline()
        if not line:
            break
        line = line.strip().split(',')
        try:
            time_ = int(line[0])
            id = int(line[1])
            size = int(line[3])
            type = int(line[13])
        except:
            continue
        # time_, id, _, size, _, _, _, _, _, _, _, _, _, type, _ = map(int, line.strip().split(','))
        if type not in types:
            num_dict[type] = 1
            types.add(type)
        else:
            num_dict[type] = num_dict.get(type, 0) + 1
    with open(output_file_path, 'w') as output_file:
        output_file.write('types\tnumber\n')
        for type in types:
            output_file.write(f'{type}\t{num_dict[type]}\n')