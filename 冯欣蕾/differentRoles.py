# there are two roles in the systerm
class worker:
    #定义共有属性

    #定义私有属性
    def __init__(self, id, balance, bid, reputation, panel_count, paticapate_count,CompletionRate, state):
        self.id = id
        self.balance = balance   #余额
        self.bid = bid
        self.reputation = float(reputation)    #初始信誉值  1.0
        self.panel_count = int(panel_count)  #未完成的次数
        self.paticapate_count = int(float(paticapate_count))  #参与的次数
        self.ComletionRate = float(CompletionRate)
        self.finish = 0
        self.state = int(state)  #-1:不在线  0 空闲已准备  1  工作中


    def cal_reputation(self,flag):#里面会改变repuatation的值
        #print("flag ",flag)
        r = self.reputation
        if flag == 0:
            if self.paticapate_count < 5:
                r = 1-0.005*self.panel_count
            else:
                r = r*(1-self.panel_count/self.paticapate_count)

        else: #表示本次成功
            r = min( r * (1+ self.panel_count/self.paticapate_count*0.5),1)
            self.reputation = round(r,2)
        return r
        #return self.reputation

    def cal_ComletionRate(self,flag): #flag 标记本次完成还是没完成
        oldR = self.reputation
        nowcr = self.cal_reputation(flag)
        #print("oldR ",oldR," nowcr ",nowcr)
        deltaRepupation = nowcr - oldR
       #print("delta credit ",deltaRepupation)
        ComletionRate = round(min((1+deltaRepupation) * self.ComletionRate,1),2)
        return ComletionRate

class teamWorker:
    def __init__(self,teamId,teamWorkers, state): #teamWorkers =[]
        self.teamId = teamId
        self.teamWorkers = teamWorkers
        self.state = state

    def addTeamWorkers(self,worker):
        self.teamWorkers.append(worker)
        if len(self.teamWorkers)>9:
            self.state = 0
        return

    def delTeam(self,worker):
        del self.teamWorkers[worker.id]
        return

    #reputation,finish_task_ratio,state,bid
    def getState(self):
        if(self.state == 0):
            return 0
        if(self.state == -1):
            return -1
        if (self.state == 1):
            return 0
    def getTeamWorkerInfo(self):
        teamReputation = 0
        teamFinishTaskRatio = 0
        teamBid = 0
        scale = len(self.teamWorkers)
        for worker in self.teamWorkers:
            teamReputation += worker.reputation
            teamFinishTaskRatio += worker.ComletionRate
            teamBid += float(worker.bid)
        teamReputation = teamReputation/scale
        teamFinishTaskRatio = teamFinishTaskRatio/scale
        teamBid = round(teamBid,2)
        return teamReputation,teamFinishTaskRatio,scale,teamBid


class Network:
    def __init__(self, vehicleTeams, timestamp):
        self.vehicleTeams = vehicleTeams
        self.timestamp = timestamp
    def addvehicleTeam(self, vehicleTeam):
        self.vehicleTeams[vehicleTeam.teamId] = vehicleTeam
        return
























