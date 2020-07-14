import random
import numpy
import math
import copy
import numpy as np

#计算z的值
def ztj(ST,N,X,Y,j,g):
    x = 1
    y = 1
    for i in range(0,N):
        x *= X[i] ** ST[i][j] * (1 - X[i]) ** (1 - ST[i][j]) * g
        y *= Y[i] ** ST[i][j] * (1 - Y[i]) ** (1 - ST[i][j]) * g
   # print("x ",x," y ",y)
    return round(x/(x + y),5)

def calxi(ST,i,Z,M):
    ztj = 0
    all = 0
    Ai = 0
    for j in range(0,M):
        if ST[i][j] == 1: #表示i参与了这个
            ztj += Z[j]
            Ai += 1
        all += Z[j]
    x = round(ztj/all,3)
    print("M  ",M ," all ",all)
    print("M - all ",M - all)
    y = round((Ai - ztj)/(M - all), 3)
    g = round(all/M, 3)
    return x, y, g


def EM_step(ST,M,N):
    max_iteration = 10
    H = [0 for x in range(0, M)]
    E = [0 for x in range(0, M)]
    # M = 5  #5个任务集
    # N = 10  #N个seller
    X = [0 for x in range(0, N)]
    Y = [0 for x in range(0, N)]
    R = [0 for x in range(0, N)]
    Z = [0 for x in range(0, M)]
    g = random.uniform(0, 1)
    #initialization EM算法的最初初始化
    for i in range(0,N):
        count = 0
        for j in range(0,M):
            if ST[i][j] == 1:
                count +=1
        R[i] = round(count/M, 2)
        X[i] = R[i]
        Y[i] = round(1-X[i],3)
    #print("X ",X)
    #print("Y ",Y)
    t = 0
    while t < max_iteration:
        for j in range(0, M):
            Z[j] = ztj(ST,N,X,Y,j,g)
        print("Z ",Z)
        for i in range(0, N):
            x, y, gi = calxi(ST,i,Z,M)
            X[i] = x
            Y[i] = y
            if g - gi <0.0001:
               t = max_iteration
               break
            g = gi
            t += 1
    for j in range(0, M):
        if Z[j] > 0.5:
            H[j] = 1  #1代表true
        else:
            H[j] = 0
    E = X
    return H,E
def RD(d):
    return 2*d
def Vq(R):
    if(R>0):
        return math.log(R)*2
    else :
        return 0
def Qij(d,b):
    k = 0
    while Vq(RD(d)+k)-Vq(k)-b > 0:
        k += 1
    if Vq(RD(d)+k)-Vq(k)-b == 0:
        return k
    else :
        return k-1
def calHithLowFj(ST, Q, N, j):
    Jhigh=Q[0][j]+RD(ST[0][j])
    Jlow = Q[0][j]
    for i in range(1,N):
        Jhigh = max(Jhigh,Q[i][j]+RD(ST[i][j]))
        Jlow = min(Jhigh,Q[i][j])
    return Jhigh,Jlow
def getWjS2(ST,j,W,S2):
    resultWjS2 = 0
    resultWj = 0

    for i in W:
        resultWjS2 += RD(ST[i][j])
        resultWj += RD(ST[i][j])
    for i in S2:
        resultWjS2 += RD(ST[i][j])
    #print("resultWjS2 ",resultWjS2)
    return resultWjS2, resultWj
def getS2MaxSocial(ST,Q,S2,j,Jguess):
    result = []
    for i in S2:
        if Q[i][j] >Jguess:
            result.append(i)
    return result

#Algorithm2 DQDA激励机制
def getWinW(ST,B,Q,j,N,w,h): #getWinW(ST, B, Q, j, N, w,H[j])

    if h == 1:
        for i in range(0, N):
            Q[i][j] = Qij(ST[i][j], B[i][j])
        Jhigh, Jlow = calHithLowFj(ST, Q, N, j)
        print("Jhigh ",Jhigh," Jlow ",Jlow)

        S2 = []
        w = []
        resultWjS2, resultWj = getWjS2(ST, j, w, S2)
        Jguess = (resultWjS2 + resultWj) / 2
        flag = 1
        while flag == 1 or (Jguess < resultWj and Jguess > resultWjS2):
            print("resultWjS2  Jguess  resultWj ",resultWjS2," ",Jguess," ",resultWj)
            S2 = []
            w = []
            Jguess = (Jhigh + Jlow) / 2
            for i in range(0, N):
                if Q[i][j] > Jguess:
                    w.append(i)
                elif Q[i][j] + RD(ST[i][j]) > Jguess:
                    S2.append(i)
                resultWjS2New, resultWjNew = getWjS2(ST, j, w, S2)
                if Jguess > resultWjS2New:
                    Jhigh = Jguess
                elif Jguess < resultWjNew:
                    Jlow = Jguess
                resultWj = resultWjNew
                resultWjS2 = resultWjS2New
            flag = 0
        getS2 = getS2MaxSocial(ST, Q, S2, j, Jguess)
        for i in getS2:
            w.append(i)
       # print("w ",w)
    return w,Q
def getPayment(ST,win,newWin,i,j,B):
    URD = 0
    UB = 0
    print("win ",win)
    print("newWin ",newWin)
    for k in win:
        URD += RD(ST[k][j])
        UB += B[k][j]
    usocial = Vq(URD)- UB
    URD = 0
    UB = 0
    for k in newWin:

        URD =URD + RD(ST[k][j])
        UB =UB + B[k][j]
    usocialNew = Vq(URD) - UB

    pij = usocial - usocialNew + B[i][j]
    print("usocial ", usocial, " usocialNew ,", usocialNew, " pij ", pij)
    return pij


def generateRandom01():
    result =np.random.uniform(1,10)
    if result < 7:
        return 1
    else:
        return 0

def getsocialP(ST,win,j,B):
    allR = 0
    allC = 0
    for i in win:
        allR +=RD(ST[i][j])
        allC +=B[i][j]
    return allR - allC
def DQDAMechanism(ST,B,M,N):
    W = {}  # 里面放的是对应每个任务到底选了谁去完成这个任务，比如任务1由 i为1，2， 3的车辆去完成这个任务
    P = numpy.zeros((N, M))
    Q = numpy.zeros((N, M))
    H, E = EM_step(ST, M, N)
    for j in range(0,M):
        W[j] = []
        w,Q = getWinW(ST, B, Q, j, N, [], H[j])
        tag = copy.deepcopy(ST)
        W[j] = w
        usocial = getsocialP(ST,W[j],j,B)
        for i in W[j]:
            for k in range(0,M):
                tag[i][k] = 0
            newW,Q1 = getWinW(tag, B, Q, j, N, [],H[j])
            print("i ",i," j ",j)
            print(W[j])
            print("newW ", newW)
            P[i][j] = usocial - getsocialP(ST,newW,j,B) + B[i][j]
    return W,P


if __name__ == '__main__':
    M = 10
    N = 20
    ST = numpy.zeros((N, M)) #10行5列
    B = numpy.zeros((N, M))
    for i in range(0,N):
        for j in range(0,M):
            ST[i][j] = generateRandom01()
            B[i][j] = round(random.uniform(0.5,2),2)
    # ST = [[1, 1, 0, 1, 1],
    #      [1, 1, 0, 1, 0],
    #      [0, 1, 0, 1, 0],
    #      [1, 1, 1, 1, 0],
    #      [1, 0, 1, 1, 0],
    #      [0, 1, 1, 1, 0]]
    # B = [[1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1]]
    print("ST ",ST)
    print("B ",B)
    W,P = DQDAMechanism(ST,B,M,N)
    print("W  ", W)
   # print("P  ",P)
