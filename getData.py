import openpyxl
import pandas as pd

from basic import get_cookie, request2, analyze_string

df = pd.read_excel("2023stu-all.xlsx")
wb = openpyxl.Workbook()
ws = wb.active

for iPerson, row in df.iterrows():
    iPerson = int(iPerson)
    cNum = row["num"]
    name = row["name"]
    sNum = row["cookieB"]
    print(cNum, name, sNum)
    text = get_cookie(sNum, cNum, name)

    # [[NailFecMODIFY]]
    selval = 217
    allsubsn = ['853', '856']

    nsub = len(allsubsn)
    allsubsn = ",".join(allsubsn)
    result = request2(selval, allsubsn, text)

    ws.cell(row=iPerson + 2, column=1, value=sNum)
    ws.cell(row=iPerson + 2, column=2, value=cNum)
    ws.cell(row=iPerson + 2, column=3, value=name)

    allData = analyze_string(result, nsub, True)
    for i, data in enumerate(allData):
        ws.cell(row=iPerson + 2, column=i + 4, value=data)
    print(allData)

wb.save("lsoutput.xlsx")  # [[NailFecMODIFY]]
