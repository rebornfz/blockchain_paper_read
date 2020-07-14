import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from heapq import *
import matplotlib
import math
class resultArray:
    def __init__(self):
        self.aimTask = 0
        self.bagNum = 0
        self.bagCost = 0
        self.bagPayment = 0
        self.greedyNum = 0
        self.greedyCost = 0
        self.greedyPayment = 0
        self.DQDANum = 0
        self.DQDACost = 0
        self.DQDAPayment = 0
class CompareAble:
                     #(aimTask, bagNum, bagCost, bagPayment,greedyNum,greedyCost,greedyPayment,DQDANum,DQDACost,DQDAPayment))
    def __init__(self, aimTask, bagNum, bagCost, bagPayment,greedyNum,greedyCost,greedyPayment,DQDANum,DQDACost,DQDAPayment):
        self.aimTask = aimTask
        self.bagNum = bagNum
        self.bagCost = bagCost
        self.bagPayment = bagPayment
        self.greedyNum = greedyNum
        self.greedyCost = greedyCost
        self.greedyPayment = greedyPayment
        self.DQDANum = DQDANum
        self.DQDACost = DQDACost
        self.DQDAPayment = DQDAPayment

    def __lt__(self, other):
        if self.aimTask > other.aimTask:
            return False
        else:
            return True
font = {'family': 'SimHei',
            'weight': 'normal',
            'size': 15,
            }
font1 = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 15,
            }
# 绘制消耗成本图形
matplotlib.rcParams['font.family']='SimSun' #字体
matplotlib.rcParams['font.size'] =15 # 调整字体大小
def showGraphCost(timestamp,bag,greedy, DQDAListCost):
    print("timestamp ",timestamp)
    fig, ax = plt.subplots()
    plt.ylim(10, 1800)
    x = list(range(len(timestamp)))
    total_width ,n = 0.6, 3
    width = total_width / n
    y_major_locator = MultipleLocator(250)
    A,=plt.plot(timestamp, bag, '-v',c='red',label='$BNTC$',linewidth='4', markersize=10)

    for i in range(len(x)):
        x[i] += width
    B,=plt.plot(timestamp, greedy,'-s',c='mediumblue',label='$MCBS$',linewidth='4', markersize=10) #red

    for i in range(len(x)):
        x[i] += width
    C,= plt.plot(timestamp, DQDAListCost,'-o', c='seagreen', label='$DQDA$',linewidth='4', markersize=10)
    #plt.plot(timestamp, DQDAListCost,c='seagreen', label='$y = DQDAListCost$')

    #plt.title("the Number of Total Cost")
    # 设置横纵坐标的名称以及对应字体格式

    plt.xlabel("任务规模")
    plt.ylabel("总成本（Social Cost）")
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    plt.tick_params(labelsize=15)
    plt.legend(handles=[A,B,C])
    plt.show()
    #fig.savefig("graph2/cost.eps", format='eps', dpi=1000)
    #plt.savefig("welfare1.eps", format='eps', dpi=1000)
    return
#最终支付图
def showGraphPayment(timestamp,bag,greedy, DQDQListPayment):
    x = list(range(len(timestamp)))
    total_width, n = 0.6, 3
    width = total_width / n
    fig, ax = plt.subplots()
    A,=plt.plot(timestamp, bag,'-v',c='red', label='$BNTC$',linewidth='4', markersize=10)

    for i in range(len(x)):
        x[i] += width
    B,=plt.plot(timestamp, greedy,'-s',c='mediumblue', label='$MCBS$',linewidth='4', markersize=10)

    for i in range(len(x)):
        x[i] += width
    C,=plt.plot(timestamp, DQDQListPayment,'-o',c='seagreen', label='$DQDA$',linewidth='4', markersize=10)
    y_major_locator = MultipleLocator(500)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    #plt.title("the Number of Total Payment")
    # 设置横纵坐标的名称以及对应字体格式
    plt.xlabel("任务规模")
    plt.ylabel("总支付（Payment）")
    plt.legend(handles=[A,B,C])
    plt.tick_params(labelsize =15)
    plt.show()
#    fig.savefig("graph2/payment.eps", format='eps', dpi=1000)
    return
# 选用的团队数量图
def showGraphTeamCount(timestamp,bag,greedy,DQDAListNum):
    fig, ax = plt.subplots()
    x = list(range(len(timestamp)))
    total_width, n = 0.6, 3
    width = total_width / n
    A=plt.bar(x, bag,width = width, fc='red', label='$BNTC$',tick_label=timestamp)
   # plt.plot(timestamp, bag, '-v')
    for i in range(len(x)):
        x[i] += width
    B=plt.bar(x, greedy,width = width, fc='mediumblue', label='$MCBS$',tick_label=timestamp)
    #plt.plot(x, greedy, '-s')
    for i in range(len(x)):
        x[i] += width
    C=plt.bar(x, DQDAListNum, width = width, fc='seagreen', label='$DQDA$',tick_label=timestamp)
    #plt.plot(x, DQDAListNum, 'o')
   # plt.title("the Number of Total TeamCount")
    # 设置横纵坐标的名称以及对应字体格式
    plt.xlabel("任务规模")
    plt.ylabel("获胜团队数量")
    plt.legend(handles=[A,B,C])
    plt.tick_params(labelsize =15)
    plt.show()
#    fig.savefig("graph2/count.eps", format='eps', dpi=1000)
    #plt.savefig("welfare1.eps", format='eps', dpi=1000)
    return
def showGraphBNTCCostPayment(timestamp,bagCost,bagPayment):
    x = list(range(len(timestamp)))
    total_width, n = 0.4, 2
    width = total_width / n
    plt.plot(timestamp, bagCost, c='royalblue', label='$BNTCCost$')
    plt.plot(timestamp, bagCost, '-v')
    for i in range(len(x)):
        x[i] += width
    plt.plot(timestamp, bagPayment, c='firebrick', label='$y = BNTCPayment$', )
    plt.plot(timestamp, bagPayment, '-v')
    #plt.title("the number of BTTCCost and BNTCPayment$")
    plt.xlabel("Task Scale")
    plt.ylabel("Fees")
    plt.legend()
    plt.tick_params(labelsize = 10)
    plt.show()
    return
def showGraphGreedyCostPayment(timestamp,greedyCost,greedyPayment):
    x = list(range(len(timestamp)))
    total_width, n = 0.8, 2
    width = total_width / n
    plt.plot(timestamp, greedyCost, c='royalblue', label='$y = MCBSCost$')
    plt.plot(timestamp, greedyCost, '-s')
    for i in range(len(x)):
        x[i] += width
    plt.plot(timestamp, greedyPayment, c='firebrick', label='$y = MCBSPayment$', )
    plt.plot(timestamp, greedyPayment, '-s')
    #plt.title("the number of greedyCost and greedyPayment")
    plt.xlabel("Task Scale")
    plt.ylabel("Fees")
    plt.legend()
    plt.tick_params(labelsize = 10)
    plt.show()
    return
def showGraphDQDACostPayment(timestamp, DQDAListCost, DQDAListPayment):
    x = list(range(len(timestamp)))
    total_width, n = 0.8, 2
    width = total_width / n
    plt.plot(timestamp, DQDAListCost, c='royalblue', label='$y = DQDACost$')
    plt.plot(timestamp, DQDAListCost, '-o')
    for i in range(len(x)):
        x[i] += width
    plt.plot(timestamp, DQDAListPayment, c='firebrick', label='$y = DQDQPayment$')
    plt.plot(timestamp, DQDAListPayment, '-o')
    #plt.title("the number of DQDACost and DQDAPayment")
    plt.xlabel("Task Scale")
    plt.ylabel("Fees")
    plt.legend()
    plt.tick_params(labelsize = 10)
    plt.show()
    return
def showOverPayment(timestamp,bagListCost, bagListPayment,greedyListCost, greedyListPayment,  DQDAListCost, DQDAListPayment):
    bagOverPayment = []
    greedyOverPayment = []
    DQDAOverPayment = []
    for i in range(0,len(bagListCost)):
        bagOver = round((bagListPayment[i] - bagListCost[i])/bagListPayment[i],2)
        bagOverPayment.append(bagOver)
        greedyOver = round((greedyListPayment[i] - greedyListCost[i])/greedyListPayment[i],2)
        greedyOverPayment.append(greedyOver)
        if DQDAListPayment[i] == 0:
            DQDAOverPayment.append(0)
        else:
            DQDAOver = round((DQDAListPayment[i] - DQDAListCost[i])/DQDAListPayment[i],2)
            DQDAOverPayment.append(DQDAOver)
    x = list(range(len(timestamp)))

    total_width, n = 0.9, 3
    width = total_width / n
    fig, ax = plt.subplots()
    A,=plt.plot(timestamp, bagOverPayment, '-v',c='red', label='$y = BNTC$',linewidth='4', markersize=10)
    plt.ylim(0, 1)
    for i in range(len(x)):
        x[i] += width
    B,=plt.plot(timestamp, greedyOverPayment,'-s', c='mediumblue', label='$y = MCBS$',linewidth='4', markersize=10)

    for i in range(len(x)):
        x[i] += width
    C,=plt.plot(timestamp, DQDAOverPayment,'-o', c='seagreen', label='$y = DQDA$',linewidth='4', markersize=10)
    y_major_locator = MultipleLocator(0.1)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    #plt.title("Over Payment Ratio of BNTC, MCBS and DQDA")
    # 设置横纵坐标的名称以及对应字体格式
    plt.xlabel("任务规模")
    plt.ylabel("超付率(OPR)")
    plt.legend(handles=[A,B,C])
    plt.tick_params(labelsize=15)
    plt.show()
    fig.savefig('graph2/overRatio.jpg', format='jpg', dpi=1000)
    return

def showSocialWelfare(timestamp,bag,greedy,DQDAListNum):
    fig, ax = plt.subplots()
    plt.ylim(0, 150)
    x = list(range(len(timestamp)))
    total_width, n = 0.6, 3
    width = total_width / n
    # 设置横纵坐标的名称以及对应字体格式
    A,=plt.plot(timestamp, bag,'-v', c='red', label='$BNTC$',linewidth='4', markersize=10)

    for i in range(len(x)):
        x[i] += width
    B,=plt.plot(timestamp, greedy,'-s',c='mediumblue', label='$MCBS$',linewidth='4', markersize=10)

    for i in range(len(x)):
        x[i] += width
    C,=plt.plot(timestamp, DQDAListNum,'-o', c='seagreen', label='$DQDA$',linewidth='4', markersize=10)

   # plt.title("the Social Welfare")

    plt.xlabel("任务规模")
    plt.ylabel("社会福利（Social Welfare）")
    plt.legend(handles=[A,B,C])
    plt.tick_params(labelsize =15)
    plt.show()
    fig.savefig("graph2/welfare.jpg", format='jpg', dpi=1000)
    return

def socialWelfare(taskScale,bagCost, bagPayment, bagCount,name):
    bagSW = 0
    #print(name,"  bagPayment", bagPayment, " bagCost", bagCost, "bagPayment - bagCost :", bagPayment - bagCost)
    if bagPayment > bagCost:
        #print("big  ")
        bagSW =taskScale* 300/(0.7*bagCost + 0.2*(bagPayment - bagCost) + 0.1*bagCount)
    else:

        bagSW = taskScale* 3000/ (0.2 * bagCost - 0.7 * (bagPayment - bagCost) + 0.1*bagCount)
    return bagSW

def showFigure(resultQ):
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
        bagSocialWelfare = []
        greenSocialWelfare = []
        DQDASocialWelfare = []
        #(aimTask, bagNum, bagCost, bagPayment,greedyNum,greedyCost,greedyPayment,DQDANum,DQDACost,DQDAPayment))
        size = len(resultQ)
        r=[90,120,150,180,210,240,270,310]
        aim = 0
        while size > 0:
            mumber = heappop(resultQ)
            if aim >=8:
                break
            #print("mumber.aimTask ",mumber.aimTask)
            if mumber.aimTask ==r[aim]:
                aimTaskArray.append(mumber.aimTask)
                bagListNum.append(mumber.bagNum)
                bagListCost.append(mumber.bagCost)
                bagListPayment.append(mumber.bagPayment)
                greedyListNum.append(mumber.greedyNum)
                greedyListCost.append(mumber.greedyCost)
                greedyListPayment.append(mumber.greedyPayment)
                DQDAListNum.append(mumber.DQDANum)
                DQDAListCost.append(mumber.DQDACost)
                DQDAListPayment.append(mumber.DQDAPayment)
                bagSocialWelfare.append(socialWelfare(mumber.aimTask, mumber.bagCost, mumber.bagPayment, mumber.bagNum,"bag"))
                greenSocialWelfare.append(socialWelfare(mumber.aimTask,mumber.greedyCost, mumber.greedyPayment, mumber.greedyNum,"greedy"))
                DQDASocialWelfare.append(socialWelfare(mumber.aimTask,mumber.DQDACost, mumber.DQDAPayment, mumber.DQDANum,"DQDA"))
                aim += 1
            size -=1
        showSocialWelfare(aimTaskArray, bagSocialWelfare, greenSocialWelfare, DQDASocialWelfare)
        showGraphCost(aimTaskArray, bagListCost, greedyListCost, DQDAListCost)
        showGraphPayment(aimTaskArray, bagListPayment, greedyListPayment, DQDAListPayment)
        # showGraphBNTCCostPayment(aimTaskArray, bagListCost, bagListPayment)
        # showGraphGreedyCostPayment(aimTaskArray, greedyListCost, greedyListPayment)
        # showGraphDQDACostPayment(aimTaskArray, DQDAListCost, DQDAListPayment)
        showOverPayment(aimTaskArray, bagListCost, bagListPayment, greedyListCost, greedyListPayment, DQDAListCost,
                        DQDAListPayment)
        showGraphTeamCount(aimTaskArray, bagListNum, greedyListNum, DQDAListNum)

def getCreditResult():
    credit={}
    bagListCost=[1093.68, 1093.68, 1093.68, 1093.68, 1093.68, 1093.68, 1093.68, 1093.68, 1093.68, 1093.68, 1093.68]
    bagListPayment=[1289, 1284, 1281, 1276, 1273, 1268, 1265, 1260, 1257, 1252, 1249]
    credit[270] = [bagListCost, bagListPayment]


    bagListCost=[484.71, 484.71, 484.71, 484.71, 484.71, 484.71, 484.71, 484.71, 484.71, 484.71, 484.71]
    bagListPayment=[548, 543, 541, 536, 534, 529, 527, 522, 520, 515, 513]
    credit[120] = [bagListCost, bagListPayment]

    bagListCost=[608.06, 608.06, 608.06, 608.06, 608.06, 608.06, 608.06, 608.06, 608.06, 608.06, 608.06]
    bagListPayment=[728, 725, 722, 719, 716, 713, 710, 707, 704, 701, 698]
    credit[150] = [bagListCost, bagListPayment]

    bagListCost=[732.44, 732.44, 732.44, 732.44, 732.44, 732.44, 732.44, 732.44, 732.44, 732.44, 732.44]
    bagListPayment=[878, 873, 871, 866, 864, 859, 857, 852, 850, 845, 843]
    credit[180] = [bagListCost, bagListPayment]

    bagListCost=[857.78, 857.78, 857.78, 857.78, 857.78, 857.78, 857.78, 857.78, 857.78, 857.78, 857.78]
    bagListPayment=[1052, 1050, 1044, 1042, 1036, 1034, 1028, 1026, 1020, 1018, 1012]
    credit[210]=[bagListCost, bagListPayment]

    bagListCost=[971.92, 971.92, 971.92, 971.92, 971.92, 971.92, 971.92, 971.92, 971.92, 971.92, 971.92]
    bagListPayment=[1104, 1097, 1095, 1088, 1086, 1079, 1077, 1070, 1068, 1061, 1059]
    credit[240] = [bagListCost, bagListPayment]

    bagListCost=[1257.0, 1257.0, 1257.0, 1257.0, 1257.0, 1257.0, 1257.0, 1257.0, 1257.0, 1257.0, 1257.0]
    bagListPayment=[1513, 1510, 1504, 1501, 1495, 1492, 1486, 1483, 1477, 1474, 1468]
    credit[310] = [bagListCost, bagListPayment]
    #print(credit)
    return credit

def creditOverRatio():
    task = {}
    #task[150]=[0.134, 0.139, 0.144, 0.149, 0.154, 0.159, 0.164, 0.169, 0.174, 0.179, 0.183]
    task[180]=[ 0.1127, 0.1151, 0.12231, 0.13431, 0.15111, 0.17271]
    task[210]=[ 0.13592, 0.13858, 0.14655, 0.15983, 0.17842, 0.20233]
    task[240]=[ 0.06754, 0.06945, 0.0752, 0.08479, 0.09821, 0.11546]
    task[270]=[ 0.10697, 0.10932, 0.11635, 0.12808, 0.1445, 0.16562]
    return task

def showOwnPaymentCostCredit(bagListPayment):

    credit = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    plt.plot(credit, bagListPayment, c='royalblue', label='$y = payment$')
    plt.plot(credit, bagListPayment, '-v')
    # for i in range(len(x)):
    #     x[i] += width
    # plt.plot(credit, bagListCost, c='firebrick', label='$y = cost$', )
    # plt.plot(credit, bagListCost, '-v')

    plt.xlabel("任务规模")
    plt.ylabel("超付率")
    plt.tick_params(labelsize=10)
    plt.show()

if __name__ == '__main__':
  r = [180,210,240]#120, 150, 180, 210,,
  flag = ['-v','-o','-s']
  creditValue= [0.5,0.6,0.7,0.8,0.9,1.0]
  color = ['mediumblue','red','seagreen']
  credit = getCreditResult()
  x = list(range(len(credit)))

  fig, ax = plt.subplots()


  overPay = creditOverRatio()
  print("overPay",overPay)

  A,=plt.plot(creditValue, overPay[r[0]],flag[0], c=color[0], label='$Task Scale =$'+str(r[0]),linewidth='4',markersize=10)
  #plt.plot(creditValue, overPay[r[i]], '-v')
  B, = plt.plot(creditValue, overPay[r[1]], flag[1], c=color[1], label='$Task Scale =$' + str(r[1]), linewidth='4', markersize=10)
  C, = plt.plot(creditValue, overPay[r[2]], flag[2], c=color[2], label='$Task Scale =$' + str(r[2]), linewidth='4', markersize=10)
  plt.xlabel("车辆团队的信誉值",)
  plt.ylabel("超付率（OPR）")
  plt.legend()
  plt.legend(handles=[A,B,C])
  plt.tick_params(labelsize=15)
  #plt.savefig("creditOverPay.eps", format='eps', dpi=1000)
  plt.show()





