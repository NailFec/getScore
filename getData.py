import pandas as pd
import csv
from time import sleep
import requests

from basic import get_cookie, request1_2, request2, analyze_string

df = pd.read_excel("2023stu-all.xlsx")

# Prepare CSV output
csv_data = []
headers = ["ID", "学号", "姓名"]

# [[NailFecMODIFY]]
selval = 199
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
    
    # 添加重试机制
    max_retries = 3
    wait_time = 5
    retry_count = 0
    result = None
    
    while retry_count < max_retries:
        try:
            result = request2(selval, allsubsn, text)
            if result and not result.startswith("error") and len(result) > 10:
                break
            else:
                raise Exception("服务器返回无效数据")
        except (requests.RequestException, Exception) as e:
            retry_count += 1
            print(f"请求失败 ({retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                print(f"等待{wait_time}秒钟后重试...")
                sleep(wait_time)
            else:
                print(f"达到最大重试次数，跳过学生 {name} ({cNum})")
                continue
    
    if result is None:
        print(f"无法获取学生 {name} ({cNum}) 的数据，跳过")
        continue

    row_data = [sNum, cNum, name]

    allData = analyze_string(result, nsub, True)
    row_data.extend(allData)
    print(allData)
    
    csv_data.append(row_data)
    # sleep(0.1)

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
with open(f"lsoutput-{selval}.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(csv_data)
