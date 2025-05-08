import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties

font_paths = [
    "C:/USERS/NAIL_/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/LXGWNEOXIHEI.TTF",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
]

chinese_font = None
for font_path in font_paths:
    if os.path.exists(font_path):
        try:
            chinese_font = FontProperties(fname=font_path)
            break
        except Exception:
            pass

if chinese_font is None:
    chinese_font = FontProperties()

file_path = "output/2Bmid.xlsx"
data = pd.read_excel(file_path)

subjects = data.columns[3:14]

for subject in subjects:
    plt.figure(figsize=(8, 6))

    max_score = np.nanmax(data[subject])
    
    # 计算实际的直方图数据
    hist_data, bins = np.histogram(data[subject].dropna(), bins=20)
    max_count = np.max(hist_data)
    ylim = 0

    if max_score <= 100:
        plt.xlim(0, 100)
        ylim = 35
    elif max_score <= 150:
        plt.xlim(0, 150)
        ylim = 55

    ylim_reserve = 1

    if max_count + ylim_reserve <= ylim:
        plt.ylim(0, ylim)
    else:
        plt.ylim(0, max_count + ylim_reserve)

    print(f"sub = {subject}, max_count = {max_count}, ylim = {ylim}")

    sns.histplot(data[subject], bins=20, kde=True, color="blue")
    plt.title(f"{subject} 成绩分布图", fontsize=16, fontproperties=chinese_font)
    plt.xlabel("", fontsize=14, fontproperties=chinese_font)
    plt.ylabel("", fontsize=14, fontproperties=chinese_font)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.xticks(fontproperties=chinese_font)
    plt.yticks(fontproperties=chinese_font)

    plt.show()
