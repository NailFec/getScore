import base64
import gzip
import json

import requests


def get_cookie(sNum, cNum, name):
    text = f"0※{sNum}※3101062002320230{cNum}※{name}※0※"
    text = gzip.compress(text.encode("utf-8"))
    text = base64.b64encode(text)
    # print(text.decode("utf-8"))    # [[NailFecDEBUG]]
    return text


def get_header(text):
    return {"Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
            "Cache-Control": "no-cache", "Connection": "keep-alive",
            "Cookie": f"ASP.NET_SessionId=vwtbtzvfkiq34fwbstshuhna; USER_INFO_STU={text.decode('utf-8')}",
            "Origin": "https://semp.xinghuiyuan.com.cn", "Pragma": "no-cache",
            "Referer": "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/StatAnalysis.aspx",
            "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Content-Type": "application/x-www-form-urlencoded", "DNT": "1",
            "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"', "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"', "sec-gpc": "1"}


def request0(text):
    """get all the contests ID for a single student"""
    url = "https://semp.xinghuiyuan.com.cn/stutkYczx/SubEvaluate/Handlers/SubEvaluate.ashx?type=getexalist&date=1741962092126"
    response = requests.post(url, headers=get_header(text))
    result = response.text
    # print(result)    # [[NailFecDEBUG]]
    return result


def request1(exalist, text) -> str:
    """get all the subjects from one contest with a specific student"""
    url = "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/Handlers/ExamScore.ashx?type=getsub&date=1716095218033"
    data = {"exalist": exalist}
    response = requests.post(url, headers=get_header(text), data=data)
    result = response.text
    return result


def request1_2(exalist) -> list:
    """get all the subjects from one contest without a specific student"""
    cNum = '917'
    name = '黄相杰'
    sNum = '330'
    text = get_cookie(sNum, cNum, name)
    result1 = json.loads(request1(exalist, text))

    cNum = '742'
    name = '熊嘉炜'
    sNum = '269'
    text = get_cookie(sNum, cNum, name)
    result2 = json.loads(request1(exalist, text))

    result = list({str(item): item for item in result1 + result2}.values())
    return result


def request2(selval, allsubsn, text):
    """get a student's score with contest ID & all needed subject IDs"""
    url = "https://semp.xinghuiyuan.com.cn/stutkYczx/ExamScore/Handlers/ExamScore.ashx?type=getdata2&date=1716095218033"
    data = {"groupselTab": "1", "selval": selval, "allsubsn": allsubsn}
    response = requests.post(url, headers=get_header(text), data=data)
    result = response.text
    # print(result)  # [[NailFecDEBUG]]
    return result


def analyze_string(result, nsub, onlyUseful):
    alldata = []
    lastp = 0
    for i in range(nsub * 10):
        pa = result.find("</td><td>", lastp)
        pb = result.find("</td>", pa + 2)
        thisData = result[(pa + len("</td><td>")): pb]
        try:
            thisData = float(thisData)
        except ValueError:
            pass
        lastp = pa + 2
        if (not onlyUseful) or (0 <= i < nsub) or (3 * nsub <= i < 4 * nsub):
            alldata.append(thisData)
    return alldata
