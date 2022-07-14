import pandas as pd
import math
data1 = pd.read_csv('文化A卷.csv')
data2 = pd.read_excel('文化A卷_text.xlsx')
data3 = pd.read_excel('2道拖拽题-导入SPSS.xlsx',sheet_name='myth')
print(len(data3))
def T1(mess):
    if mess == 10 or mess == 11:
        return 1
    elif mess == 21:
        return 2
    elif mess == 31:
        return 3
    elif mess == 41:
        return 4
    elif mess == 99:
        return 0
    else:
        return None
def T3(mess):
    if mess == 10 or mess == 99:
        return 0
    elif mess == 11 or mess == 12 or mess == 13:
        return 1
    elif mess == 21 or mess == 22:
        return 2
    elif mess == 31:
        return 3
    elif mess == 41:
        return 4
    else:
        return None
def T4(mess):
    if mess == 10 or mess == 99:
        return 0
    elif mess == 11 or mess == 12:
        return 1
    elif mess == 21 or mess == 22:
        return 2
    elif mess == 31 or mess == 32:
        return 3
    elif mess == 41 or mess ==42:
        return 4
    elif mess == 51 or mess ==52:
        return 5
    else:
        return None
def T5(mess1):
    if mess1 == 99:
        t5 = 0
    else:
        t5 = mess1
    return t5
def T61(mess1):
    if mess1 == 10 or mess1 ==99:
        t6 = 0
    elif mess1 == 11 or mess1 ==10.5:
        t6 = 1
    elif mess1 == 121 or mess1 == 122 or mess1 ==11.5 or mess1 ==121.5 or mess1 == 12:
        t6 = 2
    elif mess1 == 13:
        t6 = 3
    else:
        return None
    return t6
def T62(mess1):
    if mess1 == 20 or mess1 ==99:
        t6 = 0
    elif mess1 == 21 or mess1 ==0.5 or mess1 == 20.5:
        t6 = 1
    elif mess1 == 22 or mess1 ==21.5:
        t6 = 2
    elif mess1 == 52:
        t6 = 5
    else:
        return None
    return t6
def cost_times(sta,sto):
    c_time = pd.to_timedelta(pd.to_datetime(sta,errors='coerce').astype('datetime64[ns]') - pd.to_datetime(sto,errors='coerce').astype('datetime64[ns]'))
    return c_time.dt.total_seconds()


start_time = []
stop_time = []
cost_time = []
name = []
school = []
t1 =[]
t2 =[]
t3 =[]
t4 =[]
t5 =[]
t6 =[]
t2_score = []
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
    t1.append(row_index['2-1'].values[0])
    t2.append(row_index['2-2'].values[0])
    t3.append(row_index['3-1'].values[0])
    t4.append(row_index['4-1'].values[0])
    t5.append(row_index['4-2'].values[0])
    t6.append(row_index['1-1'].values[0])
    t2_score.append(row_index2['T2'].values[0])
data1['name'] = name
data1.insert(loc= len(data1.columns), column='contest_id', value='A卷（高阶能力测试A）')
data1.insert(loc=len(data1.columns), column='start_time', value=start_time)
data1.insert(loc=len(data1.columns), column='stop_time', value=stop_time)
data1.insert(loc=len(data1.columns), column='cost_time', value=cost_time)
data1.insert(loc=len(data1.columns), column='school', value=school)
data1['T1_score'] = data1.apply(lambda x: T1(x["T1"]), axis=1)
data1.insert(loc=len(data1.columns), column='T2_score', value=t2_score)
data1['T3_score'] = data1.apply(lambda x: T3(x["T3"]), axis=1)
data1['T4_score'] = data1.apply(lambda x: T4(x["T4"]), axis=1)
data1['T5_score'] = data1.apply(lambda x: math.ceil(sum([T5(x["T51"]),T5(x["T52"]),T5(x["T53"])])), axis=1)
data1['T6_score'] = data1.apply(lambda x: sum([T61(x["T61"]),T62(x["T62"])]), axis=1)
data1 = data1.drop(['T1', 'T3','T4','T5','T51','T52','T53','T6','T61','T62'], axis=1, inplace=False)
data1.insert(loc=len(data1.columns), column='T1', value=t1)
data1.insert(loc=len(data1.columns), column='T2', value=t2)
data1.insert(loc=len(data1.columns), column='T3', value=t3)
data1.insert(loc=len(data1.columns), column='T4', value=t4)
data1.insert(loc=len(data1.columns), column='T5', value=t5)
data1.insert(loc=len(data1.columns), column='T6', value=t6)
data1['start_time'] = data1['start_time'].dt.tz_localize(None)
data1['stop_time'] = data1['stop_time'].dt.tz_localize(None)
data1.to_excel('文化A卷整理.xlsx',index=False)


