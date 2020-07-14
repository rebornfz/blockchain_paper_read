# coding: UTF-8
import check_situation_road
import matplotlib.pyplot as plt
from matplotlib.pylab import style
from matplotlib.pyplot import MultipleLocator
from differentRoles import *
import time
import csv
import bag_greedy
import optimit01bag
import deal_data2
import DQDA_Avaliable
import resultSort
from heapq import *
import matplotlib
#读入未处理的数据集
def genetatedataset(sFileName):

    # sFileName='data/testResult_final_without_space.csv'
    info = check_situation_road.open_file(sFileName)
    return info
#查看数据集的基本特征
def checkdataset(info):
    matplotlib.rcParams['font.family'] = 'SimSun'  # 字体
    matplotlib.rcParams['font.size'] = 15  # 调整字体大小

    count_info, timestamp, road_count, vehicle_all_count, everange = check_situation_road.check_data(info)
    #print(count_info)
    timestamp2, road_count2, vehicle_all_count2, everange2 = check_situation_road.returnlimitdata(count_info)
    # 绘制图形
    fig, ax = plt.subplots()
    plt.ylim(0, 40)
    A,=plt.plot(timestamp2, road_count2, c='b', label='车辆团队数量')
    B,=plt.plot(timestamp2, everange2, c='g', label='车辆团队平均规模')
    #plt.title(" Vehicle Group Count and Average Scale")
    plt.xlabel("时隙间隔")
    plt.ylabel("平均车辆团队规模")

    x_major_locator = MultipleLocator(500)
    y_major_locator = MultipleLocator(5)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    plt.tick_params(labelsize=15)
    plt.rcParams['font.sans-serif'] = ['Simhei']
    plt.legend(handles=[A,B])

    plt.show()
#    fig.savefig("graph2/vehicles.eps", format='eps', dpi=1000)
    # plt.plot(timestamp2, vehicle_all_count2, c='r', label='$y = Network Scale$')
    # plt.title("Total Number of Vehicles in the Network")
    # plt.xlabel("Timestamp")
    # plt.ylabel("value")
    # plt.legend()
    # fig.savefig("graph2/vehicles.eps", format='eps', dpi=1000)
    plt.show()

    return info
#初始化账户
def initAccount(info):
    # 将所有用户写入顾客文件，相当于注册
    accountName = 'data0-4000/wihtoutAccount0-4000.csv'
    finalAccountName = 'data0-4000/Account0-4000.csv'
    for time in info:
        for team in info[time]:
            # print(info[time][team])
            deal_data2.initwriteToCsv(info[time][team], accountName,deal_data2.get_uniform_random_number())
    withoutUserList = []
    accountFile = open(accountName, "r")
    finalAccountFile = open(finalAccountName, "a")
    resList = []
    index = 0
    vehicletitle = "vehicleId, balance, bid, reputation, panelCount, paticipateCount, CompletionRate, state"
    finalAccountFile.write(vehicletitle + "\n")
    for line in accountFile.readlines():
        index = index + 1
        rowset = line.split(",")
        # print(rowset[0])
        if rowset[0] not in resList:
            finalAccountFile.write(line)
            resList.append(rowset[0])
        # else:
        #     print(rowset[0])
    finalAccountFile.close()
    accountFile.close()
    return
#读入账户 返回的是账户worker字典
def readAccount(path,accountName):#将账户信息读取到字典中
    account = {}
    file = open(path+accountName,"r+")
    next(file)
    for line in file:
        row = line.split(",")
        #print("row ",row)
        #vehicleId, balance, bid, reputation, panelCount, paticipateCount, state
        account[row[0]]=worker(row[0],row[1],row[2],float(row[3]),row[4],row[5],row[6],row[7])
       # print(account[row[0]].id)
    #这里测试表明，2400-4000期间，一共有2086辆车在路上有记录
    #print(len(account))
    return account
#将账户中每一次工作都重新生成一个日志数据记录，每一次都是最后结果，下一次再读入上一次工作的结果，以此向下工作
def writeToAccountLogData(path, account, time, count):#'data0-4000/accountLogData/'
    #path = 'data/accountLogData/'
    ## file = open(fileName,'a',newline="")
    #w = csv.writer(file,dialect='excel')
    filename = 'accountLog_'+ str(time) + str(count)+ '.csv'
    #print("afilename ",filename)
    file = open(path+filename,'w',newline="")#覆盖
    w = csv.writer(file, dialect='excel')
    vehicletitle = ['vehicleId','balance', 'bid', 'reputation' ,'panelCount' ,'paticipateCount','CompletionRate','state']
    w.writerow(vehicletitle)
    for workerName in account:
        row = account[workerName]
        #print("row ",row.ComletionRate)
        #if 0.8- float(row.ComletionRate) >0.01:
           #print("reputation ",row.reputation,"ComletionRate ",row.ComletionRate )
        w.writerow([row.id,row.balance,row.bid,row.reputation,row.panel_count,row.paticapate_count,row.ComletionRate,row.state])
    file.close()
    return
#运行一个时刻的在线车辆网络团体
def runTimestamp(info,timestamp,account):
    totalWorkers = {}
    teams = info[str(timestamp)]
    vehicleTeams = {}     #timestamp时刻所有在线的车辆网络团体集合
    allVehicleCount = 0  # 统计现在一共有多少辆车
    teamsNum = 0  # 统计现在一共有多少个车辆网络团体
    for teamId in teams:  # 我们首先用  车道名+时间戳   命名为车辆网络团体名
        teamLenth = len(teams[teamId])  #待修改
        availiableWorkerCount = 0
        for v in teams[teamId]:
            if account[v].ComletionRate>= 0.6:
                availiableWorkerCount += 1
        #print("teamId ", teamId, " teamLenth ", teamLenth)
        #print("availiableWorkerCount ",availiableWorkerCount)
        if availiableWorkerCount >= 10:  # 这样的情况可以算作一个车辆团体
            allVehicleCount += availiableWorkerCount
            teamsNum += 1
            # 生成一个车辆团体网络
            vehicleTeam = teamWorker(teamId, [], -1)
            vecihleMembers = teams[teamId]
            for vecihleMember in vecihleMembers:
                if totalWorkers.get(vecihleMember):
                    vehicleTeam.addTeamWorkers(totalWorkers[vecihleMember])
                else:
                    # id, balance, reputation,panel_count,paticapate_count,state,bid):
                    # w = worker(vecihleMember, 0, 1, 0, 0, 0, 1)
                    totalWorkers[vecihleMember] = account[vecihleMember]
                    vehicleTeam.addTeamWorkers(totalWorkers[vecihleMember])
            vehicleTeams[vehicleTeam.teamId] = vehicleTeam
    #print("allVehicleCount ", allVehicleCount, " teamsNum ", teamsNum)
    return vehicleTeams,allVehicleCount,teamsNum
#获取每个团体可用于计算的信息
def getInfo(vehicleTeams):
    teamId = []
    taskCount = []
    Cost = []
    teamCredit = []
    for team in vehicleTeams:
        teamReputation,teamFinishTaskRatio,scale,teamBid = vehicleTeams[team].getTeamWorkerInfo()
        taskCount.append(scale)
        Cost.append(teamBid)
        teamId.append(team)
        teamCredit.append(teamReputation)

    #print("taskCount ",taskCount)
    #print("Cost ",Cost)
    return taskCount, Cost, teamId,teamCredit

if __name__ == '__main__':
    sFileName = 'data/generateDataset0-4000Withoutgap.csv'
    info = genetatedataset(sFileName)
    #查看数据集状态
    checkdataset(info)
    #初始化账户信息等，最终的账户信息存储在Account.csv文件中
    #initAccount(info)
    #读取账户信息到字典中，用于一次交易
    lastBagAccount = "Account0-4000.csv"
    #account = readAccount(lastBagAccount)
    endTime = 1001
    Time = 200
    timestamp = list(range(Time,endTime,50))

    bagListNum = []
    bagListCost = []
    bagListPayment = []
    greedyListNum = []
    greedyListCost = []
    greedyListPayment = []
    DQDAListNum = []
    DQDAListCost = []
    DQDAListPayment = []
    aimTaskArray = []
    resultQ = []


    # class resultArray:
    #     def __init__(self):
    #         self.aimTask = 0
    #         self.bagNum = 0
    #         self.bagCost = 0
    #         self.bagPayment = 0
    #         self.greedyNum = 0
    #         self.greedyCost = 0
    #         self.greedyPayment = 0
    #         self.DQDANum = 0
    #         self.DQDACost = 0
    #         self.DQDAPayment = 0
    while Time < endTime:
        count = 3
        while count > 0:
            path = "data0-4000/"
            #print("lastBagAccount ",lastBagAccount)
            account = readAccount(path,lastBagAccount)
            #####vehicleTeams中，通过调用getTeamWorkerInfo，可以有 teamReputation,teamFinishTaskRatio,scale,teamBid这么多参数
            vehicleTeams,allVehicleCount,teamsNum = runTimestamp(info, Time, account)
            taskCount, Cost, teamId, teamCredit = getInfo(vehicleTeams)
            #print("taskCount", taskCount)
            #根据现有车辆网络情况随机生成任务需求进行模拟
            #aimTask = int(allVehicleCount*round(random.uniform(0.6,0.8),2))

           # print("***************************************")
           # print("Optimit01bag result:")
            #print("taskCount ",taskCount)
            #print("Cost ",Cost)
            a = max(allVehicleCount -10*count,10) #同一时刻数据组做3次实验
            aimTask = a - a%10  # 保证任务都可以完成
            aimTaskArray.append(str(aimTask))
            #print("time  ",Time," task ",aimTask)
            # call  1.优化的背包算法
            testTask = aimTask
            bagCost,bagNum, bagResult,bagTeamResult = optimit01bag.callOptimit01bag(allVehicleCount,aimTask,teamsNum,testTask,taskCount,Cost,teamId) #(workerCount,task,subTaskCount,Cost)
            #print("bagResult ",bagResult)#都是id值
            # print("values ", bagCost)
            # print("nums ", bagNum)
            # print("content ", bagTeamResult)
            # print("***************************************")
            t = 1
            bagPayment = optimit01bag.bagPayment(allVehicleCount,bagResult, aimTask, teamsNum, testTask, taskCount, Cost, teamId, teamCredit,0.5)
            # print("In timestamp,", Time, " the winning bid teamId is ", bagTeamResult)
            # print("These teams are doing tasks for 5 seconds")
            # #time.sleep(0.5)
            # print("Tasks are finished")
            # print("The total scale of task is ", aimTask)
            getNewAccount = deal_data2.taskResult(account, bagTeamResult, vehicleTeams)
            # for a in getNewAccount:
            #     print("aaaa",str(getNewAccount[a].ComletionRate))
            bagListNum.append(bagNum)
            bagListCost.append(bagCost)
            bagListPayment.append(bagPayment)
            path = 'data0-4000/accountLogData/'
            writeToAccountLogData(path, getNewAccount, Time, count)
    #call 2.贪心算法
            greedyNum, greedyCost, greedyResult = bag_greedy.testGreedy(aimTask,teamsNum,taskCount, Cost)
            greedyPayment = bag_greedy.GreedyPeyment(allVehicleCount,teamsNum, greedyResult, aimTask, taskCount, Cost, teamCredit)
            greedyListNum.append(greedyNum)
            greedyListCost.append(greedyCost)
            greedyListPayment.append(greedyPayment)
            #print("hahaha path ",path, "time ",Time)
            #writeToAccountLogData(path,account, Time)
            #print("hahaha")
            accountName = "data/accountLog_"+str(Time)+str(count)+".csv"
            lastBagAccount = 'accountLogData/accountLog_' + str(Time) + str(count)+ ".csv"

            #print("bagCost ",bagCost," greedyCost ",greedyCost)
            #print("bagPayment ",bagPayment," greedyPayment ",greedyPayment)
    #call DQDA算法 DQDAMechanism(ST,B,N,M): N个worker M个任务
            # print("*******************************************")
            # print("DQDA Algorithm")
            # print("taskCount ",taskCount)
            # print("Cost ",Cost)
            # print("len(taskCount) ",len(taskCount))
            # print("aimTask ",aimTask)
            st = []
            for i in taskCount:
                st.append(1)
            #print("taskCount ",taskCount)
            W, P = DQDA_Avaliable.DQDAMechanism(taskCount, st, Cost, len(taskCount), aimTask)
            winnerId = []
            for k in W:
                winnerId.append(taskCount[k])
            #print("DQDAWinnerId ",winnerId)
            DQDAPayment = 0
            DQDACost = 0
            #print("task Count: ", aimTask, " paticipate worker: ", len(W))
            for i in W:
                #print("price i ", i, " P[i]: ", P[i], " B[i]: ", Cost[i])
                DQDAPayment += P[i]
                DQDACost += Cost[i]

          #  print("AllPayment: ",round(DQDAPayment,2)," AllCost: ",round(DQDACost,2))
            DQDANum = len(W)
            DQDAListNum.append(len(W))
            DQDAListCost.append(DQDACost)
            DQDAListPayment.append(DQDAPayment)
       # print("bagListCost ",bagListCost)

            # heappush(hq, CompareAble(i, v[i], w[i], v[i] / w[i]))
            heappush(resultQ,resultSort.CompareAble(aimTask, bagNum, bagCost, bagPayment,greedyNum,greedyCost,greedyPayment,DQDANum,DQDACost,DQDAPayment))
            count -=1
        Time += 50
    print("aimTaskArray ",aimTaskArray)
    resultSort.showFigure(resultQ)





    ###################总成本和总付款差距########################














