import pandas as pd

df = pd.read_excel('getgrade/zpcontent1/zp1.ycg.NailDATA.xlsx', sheet_name='main')
value_counts = df['政治面貌'].value_counts()
print(value_counts)

"""outputss: 
性别
女性    233
男性    191
---
汉族       341
维吾尔族      51
回族        12
哈萨克族       8
满族         5
朝鲜族        3
东乡族        2
柯尔克孜族      1
锡伯族        1
---
政治面貌
群众             351
中国共产主义青年团团员     66
其他               4
少先队员             3
---
籍贯
上海市         137
新疆维吾尔自治区     87
江苏省          65
浙江省          35
江西省          15
山东省          14
福建省          11
安徽省           9
河南省           9
广东省           7
湖北省           6
湖南省           4
辽宁省           3
嘉定区           3
河北省           3
黑龙江省          2
甘肃省           2
吉林省           1
赤水市           1
山西省           1
绩溪县           1
滁州市           1
重庆市           1
贵州省           1
云南省           1
四川省           1
陕西省           1
台湾省           1
宁波市           1
"""