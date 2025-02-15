import os
import csv
import sys
import subprocess
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.model_selection import train_test_split

# 每个特征集的特征数量
FEATURE_NUM = {'IS10_paraling': 1582}

'''
该文件是提取特征的，使用的是opensmile
get_feature_opensmile(): Opensmile 提取一个音频的特征

输入:
    file_path: 音频路径

输出：
    该音频的特征向量
'''


def get_feature_opensmile(config, filepath: str):
    # 用于存储一个音频的特征的 csv文件，推荐使用绝对路径
    single_feat_path = 'features/single_feature.csv'
    # Opensmile 配置文件路径：我们使用 IS10_paraling
    opensmile_config_path = os.path.join(config.opensmile_path, 'config/is09-13/IS10_paraling.conf')
    cmd3 = 'SMILExtract -C ' + opensmile_config_path + ' -I ' + filepath + ' -O ' + single_feat_path
    cmd = subprocess.Popen(cmd3, cwd=config.opensmile_path + 'bin', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True).communicate()[0]
    reader = csv.reader(open(single_feat_path, 'r'))
    rows = [row for row in reader]
    last_line = rows[-1]
    return last_line[1: FEATURE_NUM[config.opensmile_config] + 1]


'''
load_feature(): 从 .csv 文件中加载特征数据

输入:
    feature_path: 特征文件路径
    train: 是否为训练数据

输出:
    训练数据、测试数据和对应的标签
'''


def load_feature(config, feature_path: str, train: bool):
    # 加载特征数据
    df = pd.read_csv(feature_path)
    features = [str(i) for i in range(1, FEATURE_NUM[config.opensmile_config] + 1)]

    X = df.loc[:, features].values
    Y = df.loc[:, 'label'].values

    # 标准化模型路径
    scaler_path = os.path.join(config.checkpoint_path, 'SCALER_OPENSMILE.m')

    if train == True:
        # 标准化数据 
        scaler = StandardScaler().fit(X)
        # 保存标准化模型
        joblib.dump(scaler, scaler_path)
        X = scaler.transform(X)

        # 划分训练集和测试集
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
        return x_train, x_test, y_train, y_test
    else:
        # 加载标准化模型
        scaler = joblib.load(scaler_path)
        X = scaler.transform(X)
        return X


'''
get_data(): 
    提取所有音频的特征: 遍历所有文件夹, 读取每个文件夹中的音频, 提取每个音频的特征，把所有特征保存在 feature 中

输入:
    data_path: 数据集文件夹/测试文件路径
    feature_path: 保存特征的路径
    train: 是否为训练数据

输出:
    train = True: 训练数据、测试数据特征和对应的标签
    train = False: 预测数据特征
'''


# Opensmile 提取特征
def get_data(config, data_path, feature_path: str, train: bool):
    writer = csv.writer(open(feature_path, 'w',newline=''))

    first_row = ['label']
    for i in range(1, FEATURE_NUM[config.opensmile_config] + 1):
        first_row.append(str(i))
    writer.writerow(first_row)
    writer = csv.writer(open(feature_path, 'a+',newline=''))
    print('Opensmile extracting...')

    cur_dir = os.getcwd()
    print(cur_dir)
    sys.stderr.write('Curdir: %s\n' % cur_dir)
    print("ddd",data_path)
    os.chdir(data_path)

    for j, directory in enumerate(config.class_labels):
        sys.stderr.write("Started reading folder %s\n" % directory)
        print("ddd", directory)
        os.chdir(directory)
    # 读取该文件夹下的音频
        for filename in os.listdir('.'):
            print(filename)
            if not filename.endswith('wav'):
                continue
            filepath = os.path.join(os.getcwd(), filename)

            # 提取该音频的特征
            feature_vector = get_feature_opensmile(config, filepath)
            if train == True:
                label = config.class_labels.index(directory)
                feature_vector.insert(0, label)
            # 把每个音频的特征整理到一个 csv 文件中
                writer.writerow(feature_vector)
            else:
                feature_vector.insert(0, '-1')
                writer.writerow(feature_vector)
        sys.stderr.write("Ended reading folder %s\n" % directory)
        os.chdir('..')
    os.chdir('..')
    # os.chdir(cur_dir)
    print('Opensmile extract done.')

def get_new_data(config, data_path, feature_path: str,result_path2, train: bool):
    writer = csv.writer(open(feature_path, 'w',newline=''))
    writer2 = csv.writer(open(result_path2, 'w',newline=''))

    first_row = ['label']
    for i in range(1, FEATURE_NUM[config.opensmile_config] + 1):
        first_row.append(str(i))
    writer.writerow(first_row)
    writer2.writerow(['path'])
    writer = csv.writer(open(feature_path, 'a+',newline=''))
    writer2 = csv.writer(open(result_path2, 'a+', newline=''))
    print('Opensmile extracting...')

    cur_dir = os.getcwd()
    sys.stderr.write('Curdir: %s\n' % cur_dir)
    # 读取该文件夹下的音频
    filelist = os.listdir(data_path)
    filelist.sort(key=lambda x: int(x.split('.')[0].split('-')[-1]))
    for filename in filelist:
        print('切分数据',filename)
        if not filename.endswith('wav'):
            continue
        filepath = os.path.join(data_path, filename)

        # 提取该音频的特征
        feature_vector = get_feature_opensmile(config, filepath)
        writer2.writerow([filepath])
        feature_vector.insert(0, '-1')
        writer.writerow(feature_vector)
    print('Opensmile extract done.')