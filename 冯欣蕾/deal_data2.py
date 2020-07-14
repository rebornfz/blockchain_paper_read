import csv
import random
import math
import numpy as np

def getDataset():
#获取2400-4000编号的数据集
    sFileName = 'data/testResult_final_without_space.csv'
    wFileName = 'data0-4000/generateDataset0-4000.csv'
    with open(sFileName, newline='', encoding='UTF-8') as csvfile:
        rows = csv.reader(csvfile)
        file = open(wFileName,'w',newline="" )
        w = csv.writer(file,dialect='excel')

        for row in rows:
            if int(row[0]) < 4001 and int(row[0]) >= 0:
                w.writerow(row)
        file.close()

    return
def dealData():
    sFileName = 'data0-4000/generateDataset0-4000.csv'
    wFileName = 'data0-4000/generateDataset0-4000Withoutgap.csv'
    with open(sFileName, newline='', encoding='UTF-8') as csvfile:
        file = open(wFileName,'w',newline="")
        w = csv.writer(file,dialect = 'excel')
        rows = csv.reader(csvfile)
        for row in rows:
            tmp = row[1].split('#')
            nowflag = tmp[0]
            w.writerow([row[0],nowflag,row[2]])
        file.close()
    return
#完成率是80%，1代表完成，0代表失败
def generateRandom01():
    result =np.random.uniform(1,10)
    if result < 8:
        return 1
    else:
        return 0
def get_uniform_random_number():
    number = np.random.uniform(4, 4.1)
    #print(number)
    return round(number,2)
def get_normal_random_number():
    """

    :param loc: 正太分布均值
    :param scale: 正态分布标准差
    :return: 返回正太分布中获得的随机数
    """
    loc = 1.5
    scale = 10
    number = np.random.normal(loc=loc,scale=scale)
    return round(number,2)
def get_expon_random_number():
    u = np.random.uniform(1,10)
    number = math.log(u)
    return round(number,2)


#生成用户信息初始化
def initwriteToCsv(content,fileName,fun): #content 可以是列表或者字典，每次写入一行
    file = open(fileName,'a',newline="")
    w = csv.writer(file,dialect='excel')
    for cont in content:
        #vehicleId,balance,,bid,reputation,panelCount,paticipateCount,state
        bid = fun
        w.writerow([cont,0,bid,1.0,0,0,0.8,-1])
    file.close()
    return

def taskResult(account,bagTeamResult,vehicleTeams):#bagTeamResult是列表
    resultAccount = account

    for team in bagTeamResult:#team 是团队的id
        teamWorkers = vehicleTeams[team].teamWorkers
        for worker in teamWorkers:
            resultAccount[worker.id].paticapate_count += 1
            finish = 1#generateRandom01()#0.8的完成率
            if finish == 1:
                resultAccount[worker.id].finish = finish
            if finish == 0: #未完成任务panel_count
                resultAccount[worker.id].panel_count += 1

            resultAccount[worker.id].ComletionRate = resultAccount[worker.id].cal_ComletionRate(finish)
            #print("resultAccount[worker.id].ComletionRate ", resultAccount[worker.id].ComletionRate)

    return resultAccount

# if __name__ == '__main__':
#     getDataset()
#     dealData()







