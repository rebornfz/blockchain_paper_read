# coding: UTF-8
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np
import pylab as pl
import matplotlib
matplotlib.rcParams['font.family']='SimSun' #字体
matplotlib.rcParams['font.size'] =15 # 调整字体大小
def panet(flag,base,m,n,basecredit):
    credit = 0
    if flag ==0:#做错
        if n>5:

            credit = max(base*(1-(n-m)/n*basecredit),0.00)
        else:
            credit = 1-0.1*m
        print("fail credit ", credit)
    else:
       # print("m,n ",m," ",n," ",base)
        credit =min( base *(1+(n-m)/n*basecredit),1)
        print("credit ", credit)
    #credit = round(credit,3)

    return credit

def showGraphCost(flag,showCredit):
   # font_song = fm.FontProperties(fname=r"C:\Windows\Fonts\simsunb.ttf")
    print("timestamp ",flag)
    fig, ax = plt.subplots()
    plt.ylim(0, 1.5)
    x = list(range(len(flag)))

    A,=plt.plot(x, showCredit,'-s',c='red',label='$y = BNTC$',linewidth='4', markersize=10) #red
    #plt.plot(x, showCredit,'-s')
    # 设置横纵坐标的名称以及对应字体格式

    font = {'family': 'SimSun',
            'weight': 'normal',
            'size': 20,
            }
    font1 = {'family': 'SimSun',
             'weight': 'normal',
             'size': 15,
             }
    plt.xlabel(u'参与任务的总次数')
    plt.ylabel(u'车辆信誉值')
    plt.tick_params(labelsize = 15)
    plt.legend(handles=[A])
    plt.show()
    #fig.savefig("graph2/cost.eps", format='eps', dpi=1000)
if __name__ == '__main__':
   # show()
    flag = 0
    base = 1
    m = 0
    n = 0
    basecredit = 0.5
    flag2 = [1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1]
    flag1 = [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]
    i = 0
    showCredit=[]
    oldN = 0
    oldM = 0
    oldCredit = 0
    while i<len(flag2):
        n += 1
        if flag2[i]==0:
            m+=1
        base = panet(flag2[i], base, m, n, basecredit)
        i+=1
        showCredit.append(base)
    showGraphCost(flag2, showCredit)


