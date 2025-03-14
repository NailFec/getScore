import openpyxl

from basic import get_cookie, request1

wb = openpyxl.Workbook()
ws = wb.active

for tryid in range(213, 300):
    cNum = '728'
    name = '顾铭屹'
    sNum = '255'
    text = get_cookie(sNum, cNum, name)

    result = request1(tryid, text)
    if result != '[{"exasubSN":"0","subSN":"0","subName":"总分","exaSubIsExpr":"1"}]':
        print(tryid, result)
    else:
        print(tryid)
