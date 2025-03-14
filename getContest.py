import base64
import gzip

import openpyxl
import requests

from basic import get_header

wb = openpyxl.Workbook()
ws = wb.active

for tryid in range(213, 1000):
    try:
        cNum = '728'
        name = '顾铭屹'
        sNum = '255'

        text = f"0※{sNum}※3101062002320230{cNum}※{name}※0※"
        text = gzip.compress(text.encode("utf-8"))
        text = base64.b64encode(text)
        # print(text.decode("utf-8"))    # [[NailFecDEBUG]]

        url = "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/Handlers/ExamScore.ashx?type=getsub&date=1716095218033"
        data = {"exalist": tryid}
        response = requests.post(url, headers=get_header(text), data=data)
        result = response.text
        if result != '[{"exasubSN":"0","subSN":"0","subName":"总分","exaSubIsExpr":"1"}]':
            print(tryid, result)
        else:
            print(tryid)

    except Exception as e:
        print(f"NailERROR: {e}")
