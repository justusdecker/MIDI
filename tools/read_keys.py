DOC = '|KEY|VALUE|\n|---|---|\n'
with open('data.py', 'r') as f:
    DATA = f.read()
for line in DATA.splitlines():
    if ':' not in line: continue
    if 'None' in line: continue
    key, val = line.split(' : ')
    val = val.replace(',','').replace('\"','')
    DOC += f'|{key}|{val}|\n'
with open('result.md', 'w') as f:
    f.write(DOC)