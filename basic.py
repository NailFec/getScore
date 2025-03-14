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
