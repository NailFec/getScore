import pandas as pd
import csv

from basic import get_cookie, request1_2, request2, analyze_string

df = pd.read_excel("2023stu-class7.xlsx")

# Prepare CSV output
csv_data = []
headers = ["ID", "学号", "姓名"]

# [[NailFecMODIFY]]
selval = 239
subresult = request1_2(selval)
allsubsn = [item["exasubSN"] for item in subresult]

# Add subject names to headers (will be filled later)
headers.extend([""] * (len(allsubsn) * 2))

for iPerson, row in df.iterrows():
    iPerson = int(iPerson)
    cNum = row["num"]
    name = row["name"]
    sNum = row["cookieB"]
    print(cNum, name, sNum)
    text = get_cookie(sNum, cNum, name)

    nsub = len(allsubsn)
    result = request2(selval, allsubsn, text)

    row_data = [sNum, cNum, name]

    allData = analyze_string(result, nsub, True)
    row_data.extend(allData)
    print(allData)
    
    csv_data.append(row_data)

# Get subject names from the last result for headers
lastp = 0
for i in range(nsub):
    pa = result.find("</th><th>", lastp)
    pb = result.find("</th>", pa + 2)
    thisData = result[(pa + len("</th><th>")): pb]
    headers[3 + i] = thisData
    headers[3 + i + nsub] = thisData
    lastp = pa + 1

# Write to CSV
with open("lsoutput.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(csv_data)
