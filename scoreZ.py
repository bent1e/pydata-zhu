import pandas as pd
import math
data1 = pd.read_csv('文化Z卷.csv')
data2 = pd.read_excel('文化Z卷_text.xlsx')
data3 = pd.read_excel('2道拖拽题-导入SPSS.xlsx',sheet_name='hanzi')
def T2(mess):
    if mess == 99:
        return 0
    else:
        return mess
def T3(mess):
    if mess == 99:
        return 0
    else:
        return mess
t1_score = []
start_time = []
stop_time = []
cost_time = []
name = []
school = []
t1 =[]
t2 =[]
t3 =[]
for i in range(len(data1)):
    print(i)
    row_index = data2[data2['ticket_id'] == data1.loc[i]['ticket_id']]
    row_index2 = data3[data3['ticket_id'] == data1.loc[i]['ticket_id']]
    start_time.append(pd.to_datetime(row_index['start_time'].values[0]))
    stop_time.append(pd.to_datetime(row_index['stop_time'].values[0]))
    name.append(row_index['name'].values[0])
    school.append(row_index['school'].values[0])
    c_time = pd.to_timedelta(pd.to_datetime(row_index['stop_time'].values[0]) - pd.to_datetime(row_index['start_time'].values[0]))
    cost_time.append(c_time.total_seconds())
    t1.append(row_index['1-1'].values[0])
    t2.append(row_index['1-2'].values[0])
    t3.append(row_index['2-1'].values[0])
    t1_score.append(row_index2['T1'].values[0])
data1['name'] = name
data1.insert(loc= len(data1.columns), column='contest_id', value='A卷（高阶能力测试A）')
data1.insert(loc=len(data1.columns), column='start_time', value=start_time)
data1.insert(loc=len(data1.columns), column='stop_time', value=stop_time)
data1.insert(loc=len(data1.columns), column='cost_time', value=cost_time)
data1.insert(loc=len(data1.columns), column='school', value=school)
data1.insert(loc=len(data1.columns), column='T1_score', value=t1_score)
data1['T2_score'] = data1.apply(lambda x: T2(x["T2"]), axis=1)
data1['T3_score'] = data1.apply(lambda x: sum([T3(x["T31"]),T3(x["T32"]),T3(x["T33"]),T3(x["T34"]),T3(x["T35"])]), axis=1)
data1 = data1.drop(['T2', 'T3','T31','T32','T33','T34','T35'], axis=1, inplace=False)
data1.insert(loc=len(data1.columns), column='T1', value=t1)
data1.insert(loc=len(data1.columns), column='T2', value=t2)
data1.insert(loc=len(data1.columns), column='T3', value=t3)
data1['start_time'] = data1['start_time'].dt.tz_localize(None)
data1['stop_time'] = data1['stop_time'].dt.tz_localize(None)
data1.to_excel('文化Z卷整理.xlsx',index=False)

