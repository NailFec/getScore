import base64
import gzip

import openpyxl
import pandas as pd
import requests

from basic import get_header

df = pd.read_excel("2023stu-all.xlsx")
wb = openpyxl.Workbook()
ws = wb.active

for iPerson, row in df.iterrows():
    iPerson = int(iPerson)
    try:
        cNum = row["num"]
        name = row["name"]
        sNum = row["cookieB"]
        print(cNum, name, sNum)

        text = f"0※{sNum}※3101062002320230{cNum}※{name}※0※"
        text = gzip.compress(text.encode("utf-8"))
        text = base64.b64encode(text)
        # print(text.decode("utf-8"))    # [[NailFecDEBUG]]

        url = "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/Handlers/ExamScore.ashx?type=getdata2&date=1716095218033"
        data = {"groupselTab": "1", "selval": "217",  # [[NailFecMODIFY]]
                "allsubsn": "853,856"  # [[NailFecMODIFY]]
                }
        nsub = 2  # [[NailFecMODIFY]]
        response = requests.post(url, headers=get_header(text), data=data)
        result = response.text
        # print(result)  # [[NailFecDEBUG]]

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
