import pandas as pd
data1 = pd.read_csv("20220902.csv",converters = {'task_answer' : str},encoding='gbk')
data2 = pd.read_csv('20220902数学建模结果性数据.csv',converters = {'task_answer' : str},encoding='gbk')
def T2(mes):
    name = data2[data2['STU_CODE'] == str(mes)[:-1]]['STU_NAME'].tolist()
    if name == []:
        return 'name'
    else:
        print(name[0])
        return name[0]
data1['NAME'] = data1.apply(lambda x: T2(x["STU_CODE"]), axis=1)
data1.to_csv("20220902_name.csv",index=None)