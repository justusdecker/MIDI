
data = []
for status in range(0x90, 0x98, 1):
    for note in range(0x80):
        data.append(f'{hex(status)}+{note} : {None}')
DATA = '{\n' + ",\n".join(data) + '\n}'

with open('data.py', 'w') as f:
    f.write(DATA)