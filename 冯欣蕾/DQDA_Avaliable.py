import random
import numpy
import math
import copy
import numpy as np

#计算z的值
def ztj(ST,N,X,Y,g):
    x = 1
    y = 1
    for i in range(0,N):
       # print("X[i] ",X[i]," ST[i][j] ",ST[i]," (1 - X[i]) ** (1 - ST[i][j]) ",(1 - X[i]) ** (1 - ST[i]) )
        x *= X[i] ** ST[i] * (1 - X[i]) ** (1 - ST[i]) * g
        y *= Y[i] ** ST[i] * (1 - Y[i]) ** (1 - ST[i]) * g
       # print("x ",x," y ",y)
    if x + y == 0:
        return 0
    return round(x/(x + y),5)

def calxi(ST,i,Z):
    ztj = 0
    all = 0
    Ai = 0

    #if ST[i] == 1: #表示i参与了这个
    if ST[i] > 0.2:
       # print("ST[i]  ",ST[i])
        ztj += Z
        Ai += 1
    all += Z
    if all == 0:
        x = 0
    else:
        x = round(ztj/all,3)
   # print("M  ",M ," all ",all)
  #  print("M - all ",M - all)
    y = 0
    if all == 0:
        y = Ai - ztj
    if all == 1:
        g = 0
    else:
        g = all
    return x, y, g


def EM_step(ST,N):
    #print("ST ",ST,"  N  ",N)
    max_iteration = N
    H = 0
    E = 0
    # M = 5  #5个任务集
    # N = 10  #N个seller
    X = [0 for x in range(0, N)]
    Y = [0 for x in range(0, N)]
    R = [0 for x in range(0, N)]
    Z = 0
    g = random.uniform(0, 1)
   # g = 0.5
    #initialization EM算法的最初初始化
    for i in range(0,N):
        count = 0
        #if ST[i] == 1:
        #print("ST ",ST[i])
        #print("len(ST) ",len(ST), " i ",i)
        if ST[i] >0.3:
            count += 1
       # print("COUNT ",count)
        #R[i] = round(count, 2)
        R[i] = ST[i]
        X[i] = R[i]
        Y[i] = round(1-X[i],3)
    #print("X ",X)
   # print("Y ",Y)
    t = 0
    while t < max_iteration:
        Z = ztj(ST,N,X,Y,g)
        #print("Z ",Z)
        for i in range(0, N):
            x, y, gi = calxi(ST,i,Z)
            X[i] = x
            Y[i] = y
            if g - gi <0.0001:
               t = max_iteration
               break
            g = gi
            t += 1

    if Z > 0.5:
        H = 1  #1代表true
    else:
        H = 0
    E = X
    #print(" H ",H)
    #print("E ",E)
    return H,E
def RD(d):#data quality
    return 10*math.sqrt(d)
def Vq(R,M): #M代表任务规模
    if(R>1):
        return math.log(R)*M*150
    else :
        return 0
def Qij(d,b,M):
    k = 0
    for i in range(0,1000):
        if Vq(RD(d)+k,M)-Vq(k,M)-b > 0:
            k += 1

        if Vq(RD(d)+k,M)-Vq(k,M)-b == 0:
            return k

    return max(k-1,0)
def calHithLowFj(ST, Q, N):
    Jhigh=Q[0]+RD(ST[0])
    Jlow = Q[0]
    for i in range(1,N):
        Jhigh = max(Jhigh,Q[i]+RD(ST[i]))
        Jlow = max(min(Jlow,Q[i]),0)
    return Jhigh,Jlow
def getWjS2(ST,W,S2):
    resultWjS2 = 0
    resultWj = 0
    #print("S2  ",S2)
    for i in W:
        resultWjS2 += RD(ST[i])
        resultWj += RD(ST[i])
    for i in S2:
        resultWjS2 += RD(ST[i])
   # print("resultWjS2       ",resultWjS2)
    return resultWjS2, resultWj
def getS2MaxSocial(ST,Q,S2,Jguess):
    result = []
    for i in S2:
        if Q[i] >Jguess/4:
            result.append(i)

    return result

#Algorithm2 DQDA激励机制
def getWinW(taskCount,ST,B,Q,N,w,h,M): #getWinW(ST, B, Q, j, N, w,H[j])

    if h == 1:
        for i in range(0, N):
            Q[i] = Qij(ST[i], B[i],M)
        #print("Q ",Q)
        Jhigh, Jlow = calHithLowFj(ST, Q, N)
        #print("Jhigh ",Jhigh," Jlow ",Jlow)
        S2 = []
        w = []
        resultWjS2, resultWj = getWjS2(ST, w, S2)
        Jguess = (resultWjS2 + resultWj) / 2
        flag = 1

        while flag == 1 or (Jguess > resultWj and Jguess < resultWjS2):

            S2 = []
            w = []
            #print("jguess ", Jguess)
            Jguess = (Jhigh + Jlow) / 2

            for i in range(0, N):
                if Q[i] > Jguess:
                    w.append(i)
                elif Q[i] + RD(ST[i]) > Jguess:
                    S2.append(i)
            # print("S2",S2)
            # print("www  ",w)
            resultWjS2New, resultWjNew = getWjS2(ST, w, S2)
            # print("Jlow ",Jlow," Jhigh ",Jhigh)
            # print("resultWjS2New   resultWjNew ", resultWjS2New, " ", resultWjNew)
            if Jguess > resultWjS2New:
                Jhigh = Jguess
            elif Jguess < resultWjNew:
                Jlow = Jguess
            if resultWj == resultWjNew and resultWjS2 == resultWjS2New:
                break
            resultWj = resultWjNew
            resultWjS2 = resultWjS2New
            flag = 0
            #print("Jhigh ",Jhigh," Jlow ",Jlow)
        #print("Jguess ",Jguess)
        getS2 = getS2MaxSocial(ST, Q, S2, Jguess)
        #print("w ",w)
        for i in getS2:
            w.append(i)
       # print("w and S2 ", w)
    return w,Q
def getPayment(taskCount,ST,win,newWin,i,B):
    URD = 0
    UB = 0
    #print("win ",win)
    #print("newWin ",newWin)
    for k in win:
        URD += RD(ST[k])
        UB += B[k]
    usocial = Vq(URD)- UB
    URD = 0
    UB = 0
    for k in newWin:

        URD =URD + RD(ST[k])
        UB =UB + B[k]
    usocialNew = Vq(URD) - UB

    pij = (usocial - usocialNew )/10#+ B[i]
    print("usocial ", usocial, " usocialNew ,", usocialNew, " pij ", pij)
    return pij


def generateRandom01():
    result =np.random.uniform(1,10)
    if result < 9:
        return 1
    else:
        return 0

def getsocialP(taskCount,ST,win,B):
    allR = 0
    allC = 0

    for i in win:
        allR +=RD(ST[i])*taskCount[i]
        allC +=B[i]
   # print(" allR ",allR," allC ",allC)
    return round(allR - allC,2)
#taskCount, st, Cost, len(taskCount), aimTask
def DQDAMechanism(taskCount, ST, B, N, M):
   # W = {}  # 里面放的是对应每个任务到底选了谁去完成这个任务，比如任务1由 i为1，2， 3的车辆去完成这个任务
    P = numpy.zeros(N)
    Q = numpy.zeros(N)
    H, E = EM_step(ST,N)
    w,Q1 = getWinW(taskCount, ST, B, Q, N, [], H, M)
    #print("len(ST) ",len(ST)," N " ,N)
    tag = copy.deepcopy(ST)
   #print("w ",w) #都是获胜者的在数组中的位置
    usocial = getsocialP(taskCount,ST,w,B)
    #print("usocial ",usocial)
    for i in w:
        #tag[i] = taskCount[i]
        newtaskCount = []
        newST = []
        newB = []

        for r in range(0,len(taskCount)):
            if i != r:
                newtaskCount.append(taskCount[r])
                newST.append(1)
                newB.append(B[r])


        #print("len(newST) ", len(newST)," ", N-1)
        newH, newE = EM_step(newST, N -1)
        #print("xxxxxxxxxxxxxxxxxxxxxxxx")
        #print("newH ",newH," newE ",newE," tag ",tag)
        newW,Q1 = getWinW(newtaskCount, newST, newB, Q1, N - 1 , [], newH, M)
       # print("i ",i," j ",j)
        #print(W)
       # print("newW ", newW)
        newSocial = getsocialP(newtaskCount,newST, newW, B)
        #print("i ",i," usocial: ",usocial," newSocial: ",newSocial)
        #print("B[i] ",B[i])
        P[i] =round((usocial - newSocial)/10+B[i] ,2)
        #print("P[i] ",P[i]," B[i] ",B[i])

    return w,P


# if __name__ == '__main__':
#     M = 100
#     N = 20
#     ST = numpy.zeros(N) #10行5列
#     B = numpy.zeros(N)
#     for i in range(0,N):
#         #ST[i] = generateRandom01()
#         ST[i] = round(random.uniform(0.6,1),2)
#         B[i] = round(random.uniform(0.5,2),2)
#     # ST = [[1, 1, 0, 1, 1],
#     #      [1, 1, 0, 1, 0],
#     #      [0, 1, 0, 1, 0],
#     #      [1, 1, 1, 1, 0],
#     #      [1, 0, 1, 1, 0],
#     #      [0, 1, 1, 1, 0]]
#     # B = [[1, 1, 1, 1, 1],
#     #      [1, 1, 1, 1, 1],
#     #      [1, 1, 1, 1, 1],
#     #      [1, 1, 1, 1, 1],
#     #      [1, 1, 1, 1, 1],
#     #      [1, 1, 1, 1, 1]]
#     #print("ST ",ST)
#     #print("B ",B)
#     W, P = DQDAMechanism(ST, B, N, M)
#     print("W  ", W)
#     AllPayment = 0
#     AllCost = 0
#     print("task Count: ", M, " paticipate worker: ", len(W))
#     for i in W:
#         print("price i ", i, " P[i]: ", P[i], " B[i]: ", B[i])
#         AllPayment += P[i]
#         AllCost += B[i]
#
#     print("AllPayment: ",round(AllPayment,2)," AllCost: ",round(AllCost,2))


