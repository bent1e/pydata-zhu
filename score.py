import pandas as pd
data1 = pd.read_excel('2道拖拽题学生作答0711.xlsx',sheet_name='题目1')

data2 = pd.read_excel('2道拖拽题学生作答0711.xlsx',sheet_name='题目2')
scores1 = []
scores2 = []
def sum_score1(answer):
    first = {'2','5'}
    second = {'4','2'}
    third = {'4','5','6'}
    if len(set(answer[:2]).intersection(first)) == 1:
        score1 = 1
    elif len(set(answer[:2]).intersection(first)) ==2:
        score1 = 2
    else:
        score1 = 0
    if len(set(answer[2:4]).intersection(second)) == 1:
        score2 = 1
    elif len(set(answer[2:4]).intersection(second)) ==2:
        score2 = 2
    else:
        score2 = 0
    if len(set(answer[4:6]).intersection(third)) == 1:
        score3 = 1
    elif len(set(answer[4:6]).intersection(third)) ==2:
        score3 = 2
    else:
        score3 = 0
    return score1+score2+score3
def sum_score2(answer):
    first = {'2','3'}
    second = {'1','4'}
    third = {'5','6'}
    if len(set(answer[0:3:2]).intersection(first)) == 1:
        score1 = 1
    elif len(set(answer[0:3:2]).intersection(first)) ==2:
        score1 = 2
    else:
        score1 = 0
    if len(set(answer[1:6:4]).intersection(second)) == 1:
        score2 = 1
    elif len(set(answer[1:6:4]).intersection(second)) ==2:
        score2 = 2
    else:
        score2 = 0
    if len(set(answer[3:5]).intersection(third)) == 1:
        score3 = 1
    elif len(set(answer[3:5]).intersection(third)) ==2:
        score3 = 2
    else:
        score3 = 0
    return score1+score2+score3

for i in data1['题目1']:
    if not pd.isna(i):
        answers = i.replace('[','').replace(']','').replace("'",'').replace(' ','').split(',')[:6]
        scores1.append(sum_score1(answers))
    else:
        scores1.append(0)
for i in data2['题目2']:
    if not pd.isna(i):
        answers = i.replace('[','').replace(']','').replace("'",'').replace(' ','').split(',')[:6]
        scores2.append(sum_score2(answers))
    else:
        scores2.append(0)
data1['score'] = scores1
data2['score'] = scores2
with pd.ExcelWriter('2道拖拽题.xlsx') as xlsx:
    data1.to_excel(xlsx, sheet_name="题目1")
    data2.to_excel(xlsx, sheet_name="题目2")