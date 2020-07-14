import matplotlib.pyplot as plt
import numpy as np
from heapq import *
import copy
import sys

max_int = 100000000 + 1
# N = 11 #候选团体
# S = 300

#多重背包的优化函数
def getsatisfaction(S,SA,s,content,vv,ww,i):
    if SA[s-vv[i]] ==max_int:
        return max_int

    tastc = 0
    valuec = 0
    count = 0
    for j in range(0,len(content[s-vv[i]])):
        valuec += ww[content[s - vv[i]][j]]
        count += 1
    cmax = S / 5
    cmin = 1
    count +=1
    valuec +=ww[i]
    marginsa = -((cmin-cmax-1)*valuec - count)# print("marginsa ",marginsa)
    return marginsa
def optimizationBag(aimtask,N,S,vv,ww):#optimizationbag(teamsNum, task, subTaskCount, Cost)
    content = {}
    for i in range(0, S + 2):
        content[i] = []
    SA = [max_int for x in range(0, S + 1)]
    SA[0] = 0
    for i in range(0,N):
        for j in range(S,vv[i]-1,-1):
            margina = getsatisfaction(S,SA,j,content,vv,ww,i)
            if SA[j] > margina:
                SA[j] = margina
                content[j].clear()
                content[j] = copy.deepcopy(content[j - vv[i]])
                content[j].append(i)# print("j ", j, " SA[j] ", SA[j], "  margina ", margina," i ",i," content[j] ",content[j])
    i = 0
    while i <= S:
        if SA[i] == max_int:
            j = i
            while SA[j] == max_int and j < S:
                j = j + 1
            while i < j:
                SA[i] = SA[j]
                content[i] = copy.deepcopy(content[j])
                i = i + 1
            i = j
        i = i + 1
    nums =len(content[aimtask])
    values = 0
    for i in range(0,nums):
        values += ww[content[aimtask][i]]

    return values,nums,content[aimtask]
#if __name__ == '__main__':
#optimizationBag(aimtask,N,S,vv,ww):#optimizationbag(teamsNum, task, subTaskCount, Cost)BIT
def callOptimit01bag(allVehicleCount,aimTask,teamsNum,task,subTaskCount,Cost,teamId):
    # taskCount = [10, 10, 20, 20, 30, 30, 30, 40, 40, 70, 70]   # 可完成的任务数量
    # Cost = [10, 19, 19, 19, 28, 28, 28, 37, 73, 65, 129]  # 成本
    changeTask = task
    while True:
        cost, nums, contentAimTask = optimizationBag(aimTask,teamsNum, changeTask, subTaskCount, Cost)
        # print("allVehicleCount,teamsNum, changeTask ",allVehicleCount,teamsNum, changeTask, subTaskCount)

        if task >= allVehicleCount:
            break
        if nums > 0:
            break
        changeTask += 1
    result = []
    for r in contentAimTask:
        result.append(teamId[r])
    #print("aaa")
    return round(cost, 2),nums,contentAimTask,result
#需要reputation
def bagPayment(allVehicleCount,result,aimTask,teamsNum,task,subTaskCount,Cost,teamId, teamCredit,basecredit):
    #print("bag nums ", len(result))
    #print("teamCredit ",teamCredit)组
    price = []
    resultCost = []
    # print("BagResult ",result)
    allCost = 0
    ability = 0
    for r in result:
        allCost += Cost[r]
    for r in result:
        ability += subTaskCount[r]

    lowCostPerformanceId = -1
    allocTaskCount = 0
    allocTaskCost = -1
    # print("ability ", ability, " aimTask ", aimTask)
    # print("teamId ",teamId)
    if ability > aimTask:
        lowCostPerformance = subTaskCount[result[0]]/Cost[result[0]]
        lowCostPerformanceId = 1
        for r in result: #找到性价比最低的一个，给它分配的工作最少
            if lowCostPerformance > subTaskCount[r]/Cost[r]:
                lowCostPerformanceId = r
                lowCostPerformance = subTaskCount[r]/Cost[r]
        allocTaskCount = subTaskCount[lowCostPerformanceId]-(ability - aimTask)
        allocTaskCost = allocTaskCount * Cost[r]/subTaskCount[lowCostPerformanceId]
         #实际给性价比最低的团体分配的任务数量
    for r in result:
        # print("aimTask ",aimTask," allVehicleCount - subTaskCount[r] ",allVehicleCount - subTaskCount[r])
        if lowCostPerformanceId != -1 and r == lowCostPerformanceId:  #支付多余得能力，性价比最低得那个得定价

            if aimTask > allVehicleCount - allocTaskCount: #表示缺少这个团体，无法完成这个任务，说明很重要，所以得多给点利润
                p = allocTaskCount * (allCost / aimTask) * 1.2+(teamCredit[r]-basecredit )*5
                price.append(round(p))
                resultCost.append(Cost[r])
                continue
        if aimTask > allVehicleCount - subTaskCount[r]:  # 表示缺少这个团体，无法完成这个任务，说明很重要，所以得多给点利润
            p = subTaskCount[r] * (allCost / aimTask) * 1.2+(teamCredit[r]-basecredit )*5
            price.append(round(p))
            resultCost.append(Cost[r])
            continue
        vv = []  # 可完成的任务数量
        ww = []  # 成本
        for i in range(0, teamsNum):  # 除去已经选中的一个任务组
            if i != r:
                vv.append(subTaskCount[i])
                ww.append(Cost[i])

        cost,nums,cont,teamCont = callOptimit01bag(allVehicleCount,aimTask, teamsNum - 1, task, vv, ww, teamId)
       # print("cont ", cont)
        #print("cont[0] ",cont[0])#,"v", v[int(cont[0])],"w",[int(cont[0])]
        maximal = Cost[int(cont[0])] / subTaskCount[int(cont[0])]
        # print("len(cont) ",len(cont))
        for j in cont:
            maximal = max(maximal, Cost[j] / subTaskCount[j])  # 找到比值最大的一个，也就是完成的任务与成本比值最不合适的
        # print("meanrw ",meanrw," maximal ",maximal)
        if lowCostPerformanceId != -1 and r == lowCostPerformanceId:
            p = allocTaskCount * (cost / aimTask + maximal) * 0.5 + (teamCredit[r]-basecredit )*5
        else:
            p = subTaskCount[r] * (cost / aimTask + maximal) * 0.5 + (teamCredit[r]-basecredit )*5
        #p = subTaskCount[r] *(cost / aimTask)
        #print("p  ",p)
        price.append(round(p))
        resultCost.append(Cost[r])
    totalPayment = 0
    # print("bagPrice ",price)
    # print("bagCost ",resultCost)
    for p in price:
        totalPayment += p

    return totalPayment

def bagPaymentChangeCredit(allVehicleCount,result,aimTask,teamsNum,task,subTaskCount,Cost,teamId, teamCredit,basecredit):
    #print("bag nums ", len(result))
    #print("teamCredit ",teamCredit)组
    totalPrice = {}#总的

    allCost = 0
    ability = 0
    for r in result:
        allCost += Cost[r]
        totalPrice[r]=[]
        for i in range(11):
            totalPrice[r].append(0)
   # print("allcost ",allCost)
    for r in result:
        ability += subTaskCount[r]

    lowCostPerformanceId = -1
    allocTaskCount = 0
    allocTaskCost = -1
   # print("ability ", ability, " aimTask ", aimTask)
    # print("teamId ",teamId)

    lowCostPerformance = subTaskCount[result[0]]/Cost[result[0]]
    lowCostPerformanceId = 1
    for r in result: #找到性价比最低的一个，给它分配的工作最少
        if lowCostPerformance > subTaskCount[r]/Cost[r]:
            lowCostPerformanceId = r
            lowCostPerformance = subTaskCount[r]/Cost[r]


    if ability > aimTask:
        allocTaskCount = subTaskCount[lowCostPerformanceId]-(ability - aimTask)
        #allocTaskCost = allocTaskCount * Cost[r]/subTaskCount[lowCostPerformanceId]
    else:
        allocTaskCount = subTaskCount[lowCostPerformanceId]
         #实际给性价比最低的团体分配的任务数量
    for r in result:
        #print("aimTask ",aimTask," allocTaskCount "  ,allocTaskCount," allCost ",allCost)
        if lowCostPerformanceId != -1 and r == lowCostPerformanceId:  #支付多余得能力，性价比最低得那个得定价

            if aimTask > allVehicleCount - allocTaskCount: #表示缺少这个团体，无法完成这个任务，说明很重要，所以得多给点利润
                #price.append(round(p))

                for i in range(11):
                    #p = allocTaskCount* 1/lowCostPerformance + (i*0.1- 0.5) * 5
                    p = allocTaskCount *(allCost / aimTask+(i*0.1 - 0.5)**2) * 1.15
                    totalPrice[r][i]=p
                    #print("credittotalPrice[r][i] ", totalPrice[r][i], " Cost[r] ", Cost[r])
                continue
        if aimTask > allVehicleCount - subTaskCount[r]:  # 表示缺少这个团体，无法完成这个任务，说明很重要，所以得多给点利润

            # print("len(cont) ",len(cont))

            for i in range(11):
                #p = subTaskCount[r] * 1 / lowCostPerformance + (i*0.1 - 0.5) * 5
                p = subTaskCount[r] * (allCost / aimTask+(i*0.1 - 0.5)**2) * 1.15 #+ (i*0.1 - 0.5) * 5
                totalPrice[r][i] = p
                #print("credittotalPrice[r][i] ", totalPrice[r][i], " Cost[r] ", Cost[r])
            continue
        vv = []  # 可完成的任务数量
        ww = []  # 成本
        for i in range(0, teamsNum):  # 除去已经选中的一个任务组
            if i != r:
                vv.append(subTaskCount[i])
                ww.append(Cost[i])

        cost,nums,cont,teamCont = callOptimit01bag(allVehicleCount,aimTask, teamsNum - 1, task, vv, ww, teamId)
       # print("cont ", cont)
        #print("cont[0] ",cont[0])#,"v", v[int(cont[0])],"w",[int(cont[0])]
        maximal = Cost[int(cont[0])] / subTaskCount[int(cont[0])]
        # print("len(cont) ",len(cont))
        for j in cont:
            maximal = max(maximal, Cost[j] / subTaskCount[j])  # 找到比值最大的一个，也就是完成的任务与成本比值最不合适的
        # print("meanrw ",meanrw," maximal ",maximal)
        if lowCostPerformanceId != -1 and r == lowCostPerformanceId:
            for i in range(11):
                p = allocTaskCount * (cost / aimTask + maximal+(i*0.1 - 0.5)**2)* 0.5
                totalPrice[r][i] = p
                print("totalPrice[r][i]aaa ", totalPrice[r][i], " Cost[r] ", Cost[r])

        else:
            for i in range(11):
                p = subTaskCount[r] * (cost / aimTask + maximal+(i*0.1 - 0.5)**2) * 0.5  #+  * 5
                totalPrice[r][i] = p

        #print("Cost[r] ",Cost[r], "totalPrice[i] ",totalPrice[r])
        #p = subTaskCount[r] *(cost / aimTask)


    overPaymentRatio = []
    for i in range(11):
        overPaymentRatio.append(0)
    # print("bagPrice ",price)
    # print("bagCost ",resultCost)
    #print("totalPrice ", totalPrice)
    i=0
    for i in range(11):
        a = 0
        for r in result:
            a += totalPrice[r][i]
            print("totalPrice[r][i] ", totalPrice[r][i], " Cost[r] ", Cost[r])

        print("totalPayment ",a," totalcost ",allCost)

        overPaymentRatio[i]=round((a-allCost)/allCost,5)
        i+=1
    return overPaymentRatio

# if __name__ == '__main__':
#     vv = [32, 14, 43, 34, 16, 22, 13, 64, 34, 10]
#     ww =  [41.0, 16.82, 57.82, 44.03, 20.4, 27.91, 15.13, 83.94, 46.97, 10.51]
#     aimtask = 280
#     teamId =  ['-23185864', '135982505', '23210836', '23213604', '23275345', '23288787', '292179033', '35016111', '39673908', '41277870', '43469298']
#     cost,nums,cont,teamCont = callOptimit01bag(282, 280, 10, 280, vv, ww, teamId)
#     print (" cont ", cont)