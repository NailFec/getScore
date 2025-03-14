import base64
import gzip

import openpyxl
import pandas as pd
import requests

df = pd.read_excel("2023stu-all.xlsx")
wb = openpyxl.Workbook()
ws = wb.active

for iPerson, row in df.iterrows():
    iPerson = int(iPerson)
    try:
        # Part 1: get data from Excel
        cNum = row["num"]
        name = row["name"]
        sNum = row["cookieB"]
        print(cNum, name, sNum)

        # Part 2: turn cookieB to gzip
        text = f"0※{sNum}※3101062002320230{cNum}※{name}※0※"
        text = gzip.compress(text.encode("utf-8"))
        text = base64.b64encode(text)
        # print(text.decode("utf-8"))    # [[NailFecDEBUG]]

        # Part 3: get request content
        url = "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/Handlers/ExamScore.ashx?type=getdata2&date=1716095218033"
        headers = {"Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
                   "Cache-Control": "no-cache", "Connection": "keep-alive",
                   "Cookie": f"ASP.NET_SessionId=vwtbtzvfkiq34fwbstshuhna; USER_INFO_STU={text.decode('utf-8')}",
                   "Origin": "https://semp.xinghuiyuan.com.cn", "Pragma": "no-cache",
                   "Referer": "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/StatAnalysis.aspx",
                   "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
                   "Content-Type": "application/x-www-form-urlencoded", "DNT": "1",
                   "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                   "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-gpc": "1"}
        data = {"groupselTab": "1", "selval": "217",  # [[NailFecMODIFY]]
                "allsubsn": "853,856"  # [[NailFecMODIFY]]
                }
        nsub = 2  # [[NailFecMODIFY]]
        response = requests.post(url, headers=headers, data=data)
        result = response.text
        print(result)    # [[NailFecDEBUG]]

        # Part 4: find out the useful info
        ws.cell(row=iPerson + 2, column=1, value=sNum)
        ws.cell(row=iPerson + 2, column=2, value=cNum)
        ws.cell(row=iPerson + 2, column=3, value=name)
        allData = []
        lastp = 0
        onlyUseful = False  # [[NailFecMODIFY]]
        for i in range(nsub * 10):
            pa = result.find("</td><td>", lastp)
            pb = result.find("</td>", pa + 2)
            thisData = result[(pa + len("</td><td>")): pb]
            try:
                thisData = float(thisData)
            except ValueError:
                pass
            lastp = pa + 2
            if (not onlyUseful) or (0 <= i < nsub) or (3 * nsub - 4 <= i < 4 * nsub - 4):
                allData.append(thisData)
                ws.cell(row=iPerson + 2, column=i + 4, value=thisData)
        print(allData)

    except Exception as e:
        print(f"NailERROR on index {iPerson}: {e}")

wb.save("lsoutput.xlsx")  # [[NailFecMODIFY]]
