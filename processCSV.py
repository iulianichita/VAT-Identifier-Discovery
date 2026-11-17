from pathlib import Path
script_dir = Path(__file__).resolve().parent
file_path = script_dir / "BasicCompanyData-2026-11-01-part1_7" / "BasicCompanyData-2026-11-01-part1_7.csv"

import csv

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    content = list(reader)
    # print(content[1])
    
# print('No rows in the sample:', len(content))

r = 0
for row in content:
    if row[0] == '"K" LINE HOLDING (EUROPE) LIMITED':
        print('---- Row', r, '----')
        for i, column in enumerate(content[0]):
            if len(row[i]) != 0:
                print(column.strip(), ':', row[i])
        break
    r = r + 1