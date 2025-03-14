import pandas as pd

df_oridata = pd.read_excel('getgrade/zpcontent1/oridata.xlsx', header=None)
data = []

k = 1
while True:
    try:
        row_data = []
        # i行为0，从0开始
        row_data.append(df_oridata.iloc[10*k+2, 1])
        row_data.append(df_oridata.iloc[10*k+2, 3])
        row_data.append(df_oridata.iloc[10*k+3, 1])
        row_data.append(df_oridata.iloc[10*k+3, 3])
        row_data.append(df_oridata.iloc[10*k+3, 5])
        row_data.append(df_oridata.iloc[10*k+9, 0])
        data.append(row_data)
        k += 1
    except IndexError:
        break

df_output = pd.DataFrame(data)
df_output.to_excel('getgrade/zpcontent1/output.xlsx', index=False, header=False)