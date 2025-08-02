import json
import csv

import pandas as pd

from basic import get_cookie, request0, request1, request2, analyze_string

df = pd.read_excel("2023stu-all.xlsx")

# Prepare CSV output
csv_data = []

cNum = int(input("input cNum: "))
if cNum == 1:
    cNum = 728

row = df[df["num"] == cNum]
if not row.empty:
    name = row["name"].values[0]
    sNum = row["cookieB"].values[0]
else:
    print(f"cNum {cNum} not found")
    exit(0)

text = get_cookie(sNum, cNum, name)

result = request0(text)
result = json.loads(result)
result = result["rows"]

iExam = 0
for exam in result:
    iExam += 1
    sn = exam["sn"]
    name = exam["name"]
    print(sn, name)
    
    row_data = [sn, name]

    result = request1(sn, text)
    result = json.loads(result)

    allsubname = []
    allsubsn = []
    for eexam in result:
        subSN = eexam["subSN"]
        subName = eexam["subName"]
        exasubSN = eexam["exasubSN"]
        exaSubIsExpr = eexam["exaSubIsExpr"]
        allsubname.append(subName)
        allsubsn.append(exasubSN)
    nsub = len(allsubsn)
    allsubsn = ",".join(allsubsn)
    # print(allsubsn)    # [[NailFecDEBUG]]

    result = request2(sn, allsubsn, text)

    allData = analyze_string(result, nsub, True)
    
    # Add subject names and data to row
    row_data.extend(allsubname)
    row_data.extend(allData)
    
    csv_data.append(row_data)
    print(allsubname)
    print(allData)

# Write to CSV
with open("lsoutput.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)
