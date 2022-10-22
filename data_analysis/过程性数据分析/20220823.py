import pandas as pd
import demjson3
import csv
'''
该文件根据整合后的数据表生成过程性数据
'''
data1 = pd.read_excel("20220822.xlsx",converters = {'ticket_id' : str,'task_answer' : str})
column_data = pd.read_excel("20220818数学建模专题过程性数据分析——变量名称.xlsx")
'''
修改数据，将null修改成是page=0，即题目的首页
'''
def T2(mes):
    mid_answer1 = demjson3.decode(mes.replace("null", "{'data':{'page':0,'answer':[]},'isAnswered': false}"))['frame']['data']['page']
    return mid_answer1
def T1(mes):
    mid_answer2 = demjson3.decode(mes.replace("null", "{'data':{'page':0,'answer':[]},'isAnswered': false}"))['frame']['data']['answer']
    return mid_answer2
column_name = column_data["变量名称"].tolist()
print(column_name)
print(len(column_name))
tickid = data1['ticket_id'].unique()
task = ['运动会问题','生活水平问题']
task_page = [8,9]
writer = csv.writer(open('20220922.csv', 'w', newline=''))
writer.writerow(column_name)
writer = csv.writer(open('20220922.csv', 'a', newline=''))
'''
遍历每个学号，再遍历每个问题
'''
for tick_id in tickid:
    print(len(tickid), tickid.tolist().index(tick_id))
    break_flag = False
    for task_name in task:
        k = False
        # 记录当前两次行为的页数
        is_in_page = {"True": []}
        # 判断是否记录时间
        to_record_time = [False for i in range(task_page[task.index(task_name)])]
        # 判断是否第一次进入该题
        first_in_page = [False for i in range(task_page[task.index(task_name)])]
        # 同上
        first_in_topic = [True for i in range(task_page[task.index(task_name)])]
        # 判断是否有写入行为
        is_write_answer = [False for i in range(task_page[task.index(task_name)])]
        # 记录开始时间
        start_time = [0 for i in range(task_page[task.index(task_name)])]
        # 记录上一次的答案
        last_answer = [0 for i in range(task_page[task.index(task_name)])]
        # 记录进入该页面的开始时间
        page_strat_time = [0 for i in range(task_page[task.index(task_name)])]
        # 七个指标（主要输出目标）
        exec('stay_{}_number = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)])]))
        exec('before_{}_time = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)])]))
        exec('stay_{}_time = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)])]))
        exec('after_{}_time = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)])]))
        exec('page_{}_all_time = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)])]))
        exec('choice_change_{}_all = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)]-2)]))
        exec('choice_change_{}_after = {}'.format(task.index(task_name), [-1 for i in range(task_page[task.index(task_name)]-2)]))
        # 遍历某个学号某个问题的所有数据
        for index, row in data1[(data1['ticket_id'] == tick_id) & (data1['task_name'] == task_name)].iterrows():
            # 判断答案长度，如果大于300，视为乱作答，跳过
            if len(str(row["task_answer"])) > 300 or pd.isnull(row["task_answer"]):
                print('yes')
                break_flag = True
                break
            values = demjson3.decode(
                row["task_answer"].replace("null", "{'data':{'page':0,'answer':[]},'isAnswered': false}"))
            if "null" in row["task_answer"] and k==True:
                continue
            if "null" in row["task_answer"]:
                print(row["task_answer"])
                k = True
            if 'target' in values['frame'] or 'type' in values['frame'] or 'data' not in values['frame']:
                break_flag = True
                break
            now_time = pd.to_datetime(row["timestamp"])
            for i in range(task_page[task.index(task_name)]):
                if values['frame']['data']['page'] == i:
                    is_in_page["True"].append(i)
                    if to_record_time[i] == False:
                        start_time[i] = pd.to_datetime(row["timestamp"])
                        to_record_time[i] = True
                    if first_in_page[i] == False and i !=0:
                        first_in_page[i] = True
                        page_strat_time[i] = pd.to_datetime(row["timestamp"])
                        last_answer[i] = values['frame']['data']['answer']
                    if first_in_topic[i] == True and i != 0:
                        read_start_times = pd.to_datetime(row["timestamp"])
                        first_in_topic[i] = False
            if len(is_in_page["True"]) > 1:
                answer = values['frame']['data']['answer']
                is_write_answer[is_in_page["True"][0]] = (last_answer[is_in_page["True"][0]] == answer) #False代表有作答
                if is_in_page["True"][0] == is_in_page["True"][1]:# 绝对有作答行为
                    # print('重复停留在此页面')
                    # 删除重复的记录
                    # 如果是第一次进入题目，开始记录阅题时间
                    if first_in_topic[is_in_page["True"][0]] == False:
                        read_end_times = pd.to_datetime(row["timestamp"])
                        if task.index(task_name) == 0:
                            before_0_time[is_in_page["True"][0]] = pd.to_timedelta(read_end_times - read_start_times).total_seconds()
                            first_in_topic[is_in_page["True"][0]] = 'finish'
                        else:
                            before_1_time[is_in_page["True"][0]] = pd.to_timedelta(read_end_times - read_start_times).total_seconds()
                            first_in_topic[is_in_page["True"][0]] = 'finish'
                    if is_in_page["True"][0] != 0:
                        finish_start_time = pd.to_datetime(row["timestamp"])
                    is_in_page["True"].pop(-1)
                else:
                    # 计算检查时间
                    if is_in_page["True"][0] != 0 and not is_write_answer[is_in_page["True"][0]]:
                        finish_end_time = pd.to_datetime(row["timestamp"])
                        if task.index(task_name) == 0 and page_0_all_time[is_in_page["True"][0]] ==-1:
                            after_0_time[is_in_page["True"][0]] = pd.to_timedelta(finish_end_time - finish_start_time).total_seconds()
                            page_0_all_time[is_in_page["True"][0]] = pd.to_timedelta(
                                now_time - page_strat_time[is_in_page["True"][0]]).total_seconds()
                        if task.index(task_name) == 1 and page_1_all_time[is_in_page["True"][0]] == -1:
                            after_1_time[is_in_page["True"][0]] = pd.to_timedelta(finish_end_time - finish_start_time).total_seconds()
                            page_1_all_time[is_in_page["True"][0]] = pd.to_timedelta(
                                now_time - page_strat_time[is_in_page["True"][0]]).total_seconds()
                    if is_in_page["True"][0] != 0 and is_write_answer[is_in_page["True"][0]]:
                        first_in_page[is_in_page["True"][0]] = False
                        first_in_topic[is_in_page["True"][0]] = True
                    # 记录停留时间
                    if pd.to_timedelta(now_time - start_time[is_in_page["True"][0]]).total_seconds() >= 1 :
                        # print('大于一秒')
                        exec('stay_{}_number{} = stay_{}_number{} + {}'.format(task.index(task_name),[is_in_page["True"][0]], task.index(task_name),[is_in_page["True"][0]],1))
                        exec('stay_{}_time{} = stay_{}_time{} + {}'.format(task.index(task_name),[is_in_page["True"][0]], task.index(task_name),[is_in_page["True"][0]],pd.to_timedelta(now_time - start_time[is_in_page["True"][0]]).total_seconds()))
                        start_time[is_in_page["True"][0]] = 0
                        to_record_time[is_in_page["True"][0]] = False
                        is_in_page["True"].pop(0)
                    else:
                        # print('不足一秒，不计算次数')
                        start_time[is_in_page["True"][0]] = 0
                        to_record_time[is_in_page["True"][0]] = False
                        is_in_page["True"].pop(0)
        if break_flag == True:
            break
        change_all_times = [0 for i in range(task_page[task.index(task_name)])]
        # mid_data为中间变量用于记录修改的信息
        mid_data = data1[(data1['ticket_id'] == tick_id) & (data1['task_name'] == task_name)].reset_index()
        if not mid_data.empty:
            mid_data['page'] = mid_data.apply(lambda x: T2(x["task_answer"]), axis=1)
            mid_data['answer'] = mid_data.apply(lambda x: T1(x["task_answer"]), axis=1)
            if task.index(task_name) == 0:
                choice_change_0_all[0] = len(mid_data[mid_data['page'] == 1]) - 4 - 1
                choice_change_0_all[1] = len(mid_data[mid_data['page'] == 2]) - 1 - 1
                choice_change_0_all[2] = len(mid_data[mid_data['page'] == 3]) - 1 - 1
                choice_change_0_all[5] = len(mid_data[mid_data['page'] == 6]) - 1 - 1
            else:
                choice_change_1_all[0] = len(mid_data[mid_data['page'] == 1]) - 4 - 1
                choice_change_1_all[1] = len(mid_data[mid_data['page'] == 2]) - 1 - 1
                choice_change_1_all[2] = len(mid_data[mid_data['page'] == 3]) - 1 - 1
                choice_change_1_all[6] = len(mid_data[mid_data['page'] == 7]) - 4 - 1

            if task.index(task_name) == 0:
                choice_change_0_all[3] += 1
                choice_change_0_all[4] += 1
                for i in [4, 5]:
                    delete = False
                    last_len = 0
                    for index, row in mid_data[mid_data['page'] == i].iterrows():
                        if i == 4:
                            data = row['answer'][i - 1]
                            if last_len != len(data):
                                delete = True
                            if last_len != len(data) and delete == True:
                                choice_change_0_all[3] += 1
                                delete = False
                            last_len = len(data)
                        if i == 5:
                            data = row['answer'][4:9]
                            if last_len != len(" ".join(data)):
                                delete = True
                            if last_len != len(" ".join(data)) and delete == True:
                                choice_change_0_all[4] += 1
                                delete = False
                            last_len = len(" ".join(data))
            else:
                choice_change_1_all[3] += 1
                choice_change_1_all[4] += 1
                choice_change_1_all[5] += 1
                for i in [4, 5, 6]:
                    delete = False
                    last_len = 0
                    for index, row in mid_data[mid_data['page'] == i].iterrows():
                        if i == 4:
                            data = row['answer'][3:5]
                            if last_len != len(data):
                                delete = True
                            if last_len != len(data) and delete == True:
                                choice_change_1_all[i - 1] += 1
                                delete = False
                            last_len = len(data)
                        if i == 5:
                            data = row['answer'][5:7]
                            if last_len != len(" ".join(data)):
                                delete = True
                            if last_len != len(" ".join(data)) and delete == True:
                                choice_change_1_all[i - 1] += 1
                                delete = False
                            last_len = len(" ".join(data))
                        if i == 6:
                            data = row['answer'][8]
                            if last_len != len(" ".join(data)):
                                delete = True
                            if last_len != len(" ".join(data)) and delete == True:
                                choice_change_1_all[i - 1] += 1
                                delete = False
                            last_len = len(" ".join(data))
            is_finish = [-1 for i in range(task_page[task.index(task_name)])]
            is_finish_index = [False for i in range(task_page[task.index(task_name)])]# 记录是否完成第一次作答
            last = 0
            for i in range(task_page[task.index(task_name)]):
                for j in mid_data[mid_data['page'] == i].index:
                    if j == mid_data[mid_data['page'] == i].index[0]:
                        last = j
                        continue
                    if j == 0:
                        is_finish[i] = j
                        break
                    if j != last + 1 and j == mid_data[mid_data['page'] == i].index[-1]:
                        is_finish[i] = last
                        break
                    if j != last + 1:
                        is_finish[i] = last
                        # last = j
                        break
                    if j == mid_data[mid_data['page'] == i].index[-1]:
                        is_finish[i] = j
                        last = j
                        break
                    last = j
            if task.index(task_name) == 0 and -1 not in is_finish[1:-2] :
                try:
                    choice_change_0_after[0] = len(mid_data[mid_data['page'] == 1].index.tolist())-mid_data[mid_data['page'] == 1].index.tolist().index(is_finish[1])-1
                    choice_change_0_after[1] = len(mid_data[mid_data['page'] == 2].index.tolist())-mid_data[mid_data['page'] == 2].index.tolist().index(is_finish[2])-1
                    choice_change_0_after[2] = len(mid_data[mid_data['page'] == 3].index.tolist())-mid_data[mid_data['page'] == 3].index.tolist().index(is_finish[3])-1
                    choice_change_0_after[5] = len(mid_data[mid_data['page'] == 6].index.tolist())-mid_data[mid_data['page'] == 6].index.tolist().index(is_finish[6])-1
                except:
                    print('error')
            if task.index(task_name) == 1 and -1 not in is_finish[1:-1]:
                print(is_finish)
                choice_change_1_after[0] = len(mid_data[mid_data['page'] == 1].index.tolist())-mid_data[mid_data['page'] == 1].index.tolist().index(is_finish[1])-1
                choice_change_1_after[1] = len(mid_data[mid_data['page'] == 2].index.tolist())-mid_data[mid_data['page'] == 2].index.tolist().index(is_finish[2])-1
                choice_change_1_after[2] = len(mid_data[mid_data['page'] == 3].index.tolist())-mid_data[mid_data['page'] == 3].index.tolist().index(is_finish[3])-1
                choice_change_1_after[6] = len(mid_data[mid_data['page'] == 7].index.tolist())-mid_data[mid_data['page'] == 7].index.tolist().index(is_finish[7])-1
            if task.index(task_name) == 0 and -1 not in is_finish[1:-2]:
                choice_change_0_after[3] += 1
                choice_change_0_after[4] += 1
                for j in [4, 5]:
                    delete = False
                    last_len = 0
                    for index, row in mid_data[mid_data['page'] == j][mid_data[mid_data['page'] == j].index.tolist().index(is_finish[j]):].iterrows():
                        if j == 4:
                            data = row['answer'][j - 1]
                            if last_len != len(data):
                                delete = True
                            if last_len != len(data) and delete == True:
                                choice_change_0_after[3] += 1
                                delete = False
                            last_len = len(data)
                        if j == 5:
                            data = row['answer'][4:9]
                            if last_len != len(" ".join(data)):
                                delete = True
                            if last_len != len(" ".join(data)) and delete == True:
                                choice_change_0_after[4] += 1
                                delete = False
                            last_len = len(" ".join(data))

            if task.index(task_name) == 1 and -1 not in is_finish[1:-2]:
                for j in [4, 5, 6]:
                    choice_change_1_after[3] += 1
                    choice_change_1_after[4] += 1
                    choice_change_1_after[5] += 1
                    delete = False
                    last_len = 0
                    print(is_finish)
                    for index, row in mid_data[mid_data['page'] == j][mid_data[mid_data['page'] == j].index.tolist().index(is_finish[j]):].iterrows():
                        if j == 4:
                            data = row['answer'][3:5]
                            if last_len != len(data):
                                delete = True
                            if last_len != len(data) and delete == True:
                                choice_change_1_after[j - 1] += 1
                                delete = False
                            last_len = len(data)
                        if j == 5:
                            data = row['answer'][5:7]
                            if last_len != len(" ".join(data)):
                                delete = True
                            if last_len != len(" ".join(data)) and delete == True:
                                choice_change_1_after[j - 1] += 1
                                delete = False
                            last_len = len(" ".join(data))
                        if j == 6:
                            data = row['answer'][8]
                            if last_len != len(" ".join(data)):
                                delete = True
                            if last_len != len(" ".join(data)) and delete == True:
                                choice_change_1_after[j - 1] += 1
                                delete = False
                            last_len = len(" ".join(data))
    if break_flag == True:
        continue
    stay_number_data = stay_0_number[1:-1] + stay_1_number[1:-1]
    stay_number_data = [i+1 for i in stay_number_data]# 停留次数
    stay_time_data = stay_0_time[:-1] + stay_1_time[:-1]# 停留时间
    before_time_data = before_0_time[1:-1] + before_1_time[1:-1] #阅卷时间
    after_time_data = after_0_time[1:-1] + after_1_time[1:-1] #检查时间
    page_all_time_data = page_0_all_time[1:-1] + page_1_all_time[1:-1] #第一次做题所需总时间
    page_write_time = [page_all_time_data[i] - before_time_data[i] - after_time_data[i] for i in range(len(page_all_time_data))]
    page_write_time_data = [0 if i < 0.1 else i for i in page_write_time] #第一次做题所需总时间(除去阅题检查)
    choice_change_all_data = choice_change_0_all + choice_change_1_all #总修改次数
    choice_change_after_data = choice_change_0_after + choice_change_1_after#返回修改次数
    final_data = [tick_id] + ['name'] +  stay_time_data + choice_change_all_data + stay_number_data + before_time_data + after_time_data + choice_change_after_data
    print(final_data)
    writer.writerow(final_data)