import pandas as pd

#显示所有的列
pd.set_option('display.max_columns', None)

#显示所有的行
pd.set_option('display.max_rows', None)

# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)

# mid_data = pd.read_csv("mid_data.csv")
data2_1 = pd.read_excel("D:/360安全浏览器下载/20220606-18.33-数据/20220606-18.33-数据/ticket_log_PBL_testing3—过程数据.xlsx",sheet_name="Result 1")
print('1')
data2_2 = pd.read_excel("D:/360安全浏览器下载/20220606-18.33-数据/20220606-18.33-数据/ticket_log_PBL_testing3—过程数据.xlsx",sheet_name="Result 2")
print('1')
data2_3 = pd.read_excel("D:/360安全浏览器下载/20220606-18.33-数据/20220606-18.33-数据/ticket_log_PBL_testing3—过程数据.xlsx",sheet_name="Result 3")
print('1')
data2_4 = pd.read_excel("D:/360安全浏览器下载/20220606-18.33-数据/20220606-18.33-数据/ticket_log_PBL_testing3—过程数据.xlsx",sheet_name="Result 4")
print('1')
frames = []
for i in [data2_1,data2_2,data2_3,data2_4]:
    frames.append(i)
data = pd.concat(frames)
print('1')
label=['运动会问题','生活水平问题']
re_data = data[data["task_name"].isin(label)]
re_data = re_data.reset_index(drop=True)
re_data.to_excel('20220822.xlsx',index = None)