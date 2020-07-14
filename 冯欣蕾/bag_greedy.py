# encoding:utf-8
import matplotlib.pyplot as plt
import numpy as np
from heapq import *
import copy
import xlwt


# S = 300
# N = 11 #候选团体
# Num= [10000 for x in range(0,S+1)]个数
# Value = [10000 for x in range(0,S+1)] 成本

class node:
    def __init__(self, i, v, w, f):
        self.id = i
        self.v = v
        self.w = w
        self.u = f
class CompareAble:
    def __init__(self, i, v, w, f):
        self.id = i
        self.v = v
        self.w = w
        self.u = -f

    def __lt__(self, other):
        if self.u > other.u:
            return False
        else:
            return True
#选择团体算法
def bag(N,S,vv,ww):
    Num = [1000 for x in range(0, S + 1)]
    Value = [1000 for x in range(0, S + 1)]
    Num[0] = 0
    Value[0] = 0
    content = {}
    for i in range(0, S + 2):
        content[i] = []
    for i in range(0,N):
        for j in range(S,vv[i]-1,-1):
            if j >= v[i]:
                if Value[j] > Value[j - vv[i]] + ww[i]:
                    Num[j] = Num[j-vv[i]]+1
                    Value[j] = Value[j-vv[i]]+ww[i]
                    content[j].clear()
                    content[j] = copy.deepcopy(content[j - vv[i]])
                    content[j].append(i)
                    #print("add j ",i)
                elif  Value[j] == Value[j-vv[i]]+ww[i]:
                        if Num[j] > Num[j-vv[i]]+1:
                            Num[j]=Num[j-vv[i]]+1
                            content[j].clear()
                            content[j] = copy.deepcopy(content[j - vv[i]])
                            content[j].append(i)
    i = 0
    while i <= S:
        if Num[i] == 1000:
            j = i
           # print("i ", i, " j ", j)
            while Num[j] == 1000:
                j = j + 1
            while i < j:

                Num[i] = Num[j]
                Value[i] = Value[j]
                content[i] = copy.deepcopy(content[j])
                i = i + 1
            i = j
        i = i + 1
    return Value,Num,content  #返回完成任务S所用的总成本，总可完成任务团体组数以及任务组的id

#多重背包的优化函数
def getsatisfaction(s,vi,content,vv,ww):
    sa = 0
    tastc = 0
    valuec = 0
    count = 0
    for j in range(0,content[s-vi].size()):
        tastc += vv[content[s - vi][j]]
        valuec += ww[content[s - vi][j]]
        count += 1
    E = s * 0.8
    umax = s * 5
    cmax = 4
    A = pow(((tastc - E) / (S - E)), 3)
    B = pow((umax - valuec) / umax, 2)
    C = (cmax - count) / cmax
    sa = A * B * C
    return sa
def optimizationbag(N,s,vv,ww):
    content = {}
    for i in range(0, S + 2):
        content[i] = []
    SA = [-1000000 for x in range(0, S + 1)]
    newsa = 0
    for i in range(0,N):
        for j in range(S, vv[i]-1,-1):
            newsa = getsatisfaction(j, vv[i], content, v, ww)
            if SA[j] < newsa:
                SA[j] = newsa
                content[j] = content[j-vv[i]]
                content[j].clear()
                content[j] = copy.deepcopy(content[j - vv[i]])
                content[j].append(i)
    i = 0
    while i <= S:
        if Num[i] == 1000:
            j = i
            # print("i ", i, " j ", j)
            while Num[j] == 1000:
                j = j + 1
            while i < j:
                Num[i] = Num[j]
                Value[i] = Value[j]
                content[i] = copy.deepcopy(content[j])
                i = i + 1
            i = j
        i = i + 1
    nums = content[i].size()
    values = 0
    for i in range(0,nums):
        values += ww[content[S][i]]
    return values,nums,content







#确定给每个团体多少钱的算法
def paymentDetermination(result,N,s,v,w):  #result中只包含选中的id
    price = []
    for r in result:
        vv=[] #可完成的任务数量
        ww=[] #成本
        for i in range(0,N): #除去已经选中的一个任务组
            if i!=r:
                vv.append(v[i])
                ww.append(w[i])
        meanrw,meanrn,cont= bag(N-1, s, vv, ww)
        #print("cont ",cont[S])
        #print("cont[0] ",cont[0])#,"v", v[int(cont[0])],"w",w[int(cont[0])]
        maximal = w[int(cont[s][0])]/v[int(cont[s][0])]
        #print("len(cont) ",len(cont))
        for j in cont[s]:
            maximal=max(maximal,w[j]/v[j])  #找到比值最大的一个，也就是完成的任务与成本比值最不合适的
        #print("meanrw ",meanrw," maximal ",maximal)
        p = v[r]*(meanrw[s]/s + maximal)/2
        #print("p  ",p)
        price.append(round(p))

   # print("price ",price)
    return price
#选择算法Greedy
def Greedy(s,heapqueue):
    rn = 0
    rw = 0
    idset=[]
    tag = s
    h=copy.deepcopy(heapqueue)
    #print("heaqueue ", len(h))
   # hp = nsmallest(11, hq)
    while tag > 0 and len(h) > 0:
        a = heappop(h)
        rn +=1
        rw += a.w
        tag -= a.v
        idset.append(a.id)
    #print("greedy nums ",len(idset))
    return rn, rw,idset
#确定给钱的算法
def GreedyPeyment(allVehicleCount,teamCount,result,aimTask,taskCount,Cost, teamCredit):#GreedyPeyment(teamsNum, greedyResult, aimTask, taskCount, Cost)
    hq = []
    resultPay = []
    cost = []
    allCost = 0
    ability = 0
    #jprint("greedy nums ,",len(result))
    for r in result:
        allCost += Cost[r]
    for r in result:
        ability += taskCount[r]
    #print("GreedyResult ",result)
    lastOnePayment = 0
    overEmployedRatio = 0
    if ability > aimTask:
        #print("ability :", ability, " aimTask :", aimTask)
        lastOnePayment = 1

    for r in result: #对于已经选中的团体，分别计算应该给予团体的报酬
        if lastOnePayment == 1 and r == result[len(result)-1]:#是最后一个，且超付

            overEmployedRatio = (ability - aimTask)/ aimTask
        if aimTask > allVehicleCount - taskCount[r]:  # 表示缺少这个团体，无法完成这个任务，说明很重要，所以得多给点利润
            #print(3333333333333333333333333333333333333333333333)
            initial = 1
            if lastOnePayment == 1 and r == result[len(result) - 1]:
                #print("111111111111111111111111111111111111111111")
                p = taskCount[r] * (allCost / aimTask) * (2 - overEmployedRatio)
            else:
                #print("22222222222222222222222222222222222222")
                p = taskCount[r] * (allCost / aimTask) * 2
            resultPay.append(round(p))
            resultPay.append(Cost[r])
            continue

        for i in range(0, teamCount):
            if i!= r:
                heappush(hq, CompareAble(i, taskCount[i], Cost[i], taskCount[i] / Cost[i]))#CompareAble(i, v[i], w[i], v[i]/w[i]))
        rn, meanrw,cont=Greedy(aimTask, hq)
        maximal = Cost[int(cont[0])] / taskCount[int(cont[0])]
        #print("cont ",cont)
        for j in cont:
            maximal = max(maximal, Cost[j] / taskCount[j])  # 找到比值最大的一个，也就是完成的任务与成本比值最不合适的
        #print("meanrw ",meanrw," maximal ",maximal)
        p = taskCount[r] * (meanrw / aimTask + maximal) * 0.6 + (teamCredit[r]-0.5 )*10
        if lastOnePayment == 1 and r == result[len(result)-1]:#是最后一个，且超付
            #print("计算超付价格 ",overEmployedRatio)
            p = p * ( 1 )
       # p = v[r] * (meanrw/s)
        resultPay.append(round(p))
        cost.append(Cost[r])
    # print("aimTask ",aimTask)
    # print("greedy price ",resultPay)
    # print("greedy Cost ",cost)
    hq.clear()
    greedyPayment = 0
    for p in resultPay:
        greedyPayment += p

    return greedyPayment
#write_excel_xls("", "payment.csv", "greedy",whole_greedyPayment,"bag",whole_payment)
def write_excel_xls(path,sheet_name, name1,value1,name2,value2):
    index = len(value1)  # 获取需要写入数据的行数
    #print("index ",index)
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    #for i in range(0, index):
      #  print("value[i] ",len(value[i]))
    sheet.write(0, 0,name1)
    for j in range(1, len(value1)):
        sheet.write(j,0, value1[j])  # 像表格中写入数据（对应的行和列）
    sheet.write(0, 1, name2)
    for j in range(1, len(value2)):
        sheet.write(j, 1, value2[j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")
def testGreedy(S,teamsNum,testCount,Cost):
    heapqueue = []  # 优先队列
    for i in range(0, teamsNum):  # N个候选团体
        heappush(heapqueue, CompareAble(i, testCount[i], Cost[i], testCount[i] / Cost[i]))
    #print("exec Greedy :")
    # greedynum = [0 for x in range(0, S + 1)]
    # greedyValue = [0 for x in range(0, S + 1)]
    # greedyPrice = [0 for x in range(0, S + 1)]
    # whole_greedyPayment = [0 for x in range(0, S + 1)]

    # 测试  一个案例greedy
    greedyNums,greedyCost,greedyResult = Greedy(S,heapqueue)
    # print("value ", round(greedyCost,2))
    # print("num ", greedyNums)
    return greedyNums,greedyCost,greedyResult
    # # for i in range(0, len(resultg)):
    # #     print("group id ", resultg[i], " ")
    # greedyPrice = GreedyPeyment(resultg, S,testCount,Cost)
    # whole_greedyPayment = 0
    # for pay in greedyPrice:
    #     whole_greedyPayment+=pay
    # print("greedyPrice ",greedyPrice)
    # print("whole_greedy ",S,"  ",whole_greedyPayment)

# if __name__ == '__main__':
#
#     v = [10, 10, 20, 20, 30, 30, 30, 40, 40, 70, 70]   # 可完成的任务数量
#     w = [10, 19, 19, 19, 28, 28, 28, 37, 73, 65, 129]  # 成本
#
#     # hp = nsmallest(11, heapqueue)
#     # for h in hp:
#     #     print("h  ",h.id)
#
#     # 生成x步长为1的列表数据
#     task_num = np.arange(0, S+1, 1)
#     # 设置x、y坐标轴的范围
#     plt.xlim(0, S+1)
#     plt.ylim(0, 10)
#
#     print("exec 01 bag : ")
#     Value, Num, result = bag(N, S, v, w)
#     # #-------测试一个--------------
#     # PP = paymentDetermination(result[S], N, S, v, w)
#     # print("result01 ",result[S])
#     # print("pp",PP)
#     # whole_01pay=0
#     # for p in PP:
#     #     whole_01pay+=p
#     # print("01bag ",S,"  ",whole_01pay)
# #----------------------------------------------------#
# #----------------迭代测试01bag-----------------------#
#     whole_payment = [0 for x in range(0, S + 1)]
#     for i in range(1,S+1):
#         last_payment = paymentDetermination(result[i], N, i, v, w)
#         # print("last_payment ",last_payment)
#         # print("Value ", Value[i])
#         # print("Num ", Num[i])
#         # print("the count of whom take part in : ", len(result))
#
#         # for j in range(len(result[i])):
#         #     print("group id ", result[i][j])
#         for pay in last_payment:
#             whole_payment[i] += pay
#         # print("whole_payment[i] ",whole_payment[i])
# #-----------------------------------------------------#



   # #所有案例
   #  for i in range(1,S+1):
   #      greedynum[i],greedyValue[i],resultGreedy=Greedy(i,heapqueue)
   #     # print( greedynum[i],"  ",greedyValue[i])
   #      greedyPrice[i] = GreedyPeyment(resultGreedy,i,v,w)#(result,s,v,w)
   #      whole_greedyPayment[i] = 0
   #     # print("i ",i,"  greedyPrice[i] ",greedyPrice[i])
   #      for pay in greedyPrice[i]:
   #          whole_greedyPayment[i] +=pay
   #
   #      # print("greedyValue  ", greedyValue[i])
   #      # print("greedynum  ", greedynum[i])
   #
   # # write_excel_xls("payment.xls","payment", "greedy",whole_greedyPayment,"bag",whole_payment)
   #
   #
   #  for i in range(0,len(whole_payment)):
   #     print("i ",i," ",str(whole_payment[i]),"greedy ",whole_greedyPayment[i])
   #
   #
   #  # 绘制图形
   #  plt.plot(task_num, Num, c='b',label='$y = bag$' )
   #  plt.plot(task_num, greedynum, c='r',label='$y = greedy$')
   #  plt.title("the number of tasks and the number of AVC")
   #  plt.xlabel("the number of tasks")
   #  plt.ylabel("the number of AVC")
   #  plt.legend()
   #  plt.show()
   #  plt.plot(task_num, Value, c='b',label='$y = bag$')
   #  plt.plot(task_num, greedyValue, c='r',label='$y =greedy$')
   #  plt.title("the number of tasks and the whole cost")
   #  plt.xlabel("the number of tasks")
   #  plt.ylabel("the whole truth cost")
   #  plt.legend()
   #  plt.show()
   #  #最终付费总额与任务数关系
   #  print("whole_payment ",whole_payment)
   #  print("greedyPayment",whole_greedyPayment)
   #  plt.plot(task_num, whole_payment, c='b', label='$y = bag$')
   #  plt.plot(task_num, whole_greedyPayment, c='r', label='$y =greedy$')
   #  plt.title("the number of tasks and the whole payment")
   #  plt.xlabel("the number of tasks")
   #  plt.ylabel("the whole payment to workers")
   #  plt.legend()
   #  plt.show()