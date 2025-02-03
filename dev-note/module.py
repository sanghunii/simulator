##강화학습 Enviornment 구성하는 class모음
"""
1. JobClass
    각 Job
2. MachineClass (Job)   
"""

from typing import List
from random import randint
import numpy as np

class Job():
    def __init__(self, 
                 operatingNum: int = 10,  ##거쳐야 하는 operating 갯수.
                 inspected: bool = True
                 ):
        self.operatingNum = operatingNum
        self.inspected = inspected
        self.leadTimes = []
    ##operating갯수만큼 leadTime생성 
        for i in range(0, operatingNum):
            self.leadTimes.append(randint(10,30))
        
    
##Test Method => Job의 각 leadTime이 잘 생성 되는지 확인 
    def showLeadTime(self):
        for i in range(0, self.operatingNum):
            print('-------------------')
            print(f"{i +1}번째 machine lead time : ", self.leadTimes[i])

##각 단계에서 사용하는 machine에 맞는 leadtime을 가져온다.
    def getLeadTime(self, machineNum: int) -> int:
        leadTime = self.leadTimes[machineNum]

        return leadTime
        


    
 


class Machine():
    def __init__(
            self,
            job: Job = None,
            machineNum: int = 0,        ##몇번째 operating을 수행하는 machine인지 
            leadTime: int| float = 0,   ##given by Job
            ##mode: bool = False, ##False means permutation / True means nonPermutation -> 필요없어 보이는데 ? 
            inspection: bool = False,   ##True면 해당 machine은 inspection을 담당하는 machine.
            available: bool = True,     ##True면 해당 machine은 현재 job을 받을 수 있는 상태 
    ):
    ##set attributes 
        self.job = job
        self.machineNum = machineNum
        self.leadTime = leadTime
        ## self.mode = mode --> 필요없어 보이는데 ? 
        self.inspection = inspection
        self.available = available
    

##Job을 할당할때 setMachine을 이용해서 Machine을 세팅한다.
    def setMachine(
            self,
            job: Job
    ):
        self.job = job
        self.leadTime = job.getLeadTime(machineNum = self.machineNum)
        self.available = False

    
aaaa



class Environment():
    def __init__(
            self,
            mode: bool = False,
            operatingNum: int = 2,
            jobNum: int = 10,
            episode: int = 1
    ):
        self.makespan = 0 
        self.jobNum = jobNum
        self.mode = mode
        self.operatingNum = operatingNum
        
        
    ##create jobPool
        self.jobPool = []
        for i in range(0, self.jobNum):
            self.jobPool.append(Job(operatingNum= operatingNum))
        
    ##create Process
        self.process = []
        for i in range(0, operatingNum):
            self.process.append(Machine(machineNum=i))
    
    ##첫번재 job할당
        self.process[0].setMachine(self.jobPool[0])
    
    def run(self):
        ##맨 처음에 첫번째 machine에 Job투입
        pass


    def setInsepction(machineNum: int):
        pass
        """
        일단 패스 ㅎㅎ
        """
    
    #def run(self):
    #    asdf



    
        
                



        

##Test Methods
    def showMachinesState(self):
        for i in range(0, self.operatingNum):
            print("-------------------------------------")
            print(f"{i}번째 machine & job \n ")
            print(self.process[i], "\n")
            for j in range(0, self.jobNum):
                print(f"{j}번째 job의 {i}번째 machine lead time : ", self.jobPool[j].leadTimes[i])

    def showEnvInf(self):
        print('-------------------')
        print(f"mode : {self.mode}")
        print(f"operatingNum : {self.operatingNum}")
        print(f"jobNum: {self.jobNum}")
        print(f"makespan : {self.makespan}")
        print('-------------------')
    


"""
    def updateProcess(self):
    ##현재 job이 할당된 machine이 있는지 확인
        for i in range(0, self.operatingNum):
            state = False
            if self.process[i].available is False:
                state = True 

    ##job이 할당된 machine이 있으면 lead
"""



"""
machine갱신 logic:
    전체 시간 -1
    makespan += 1
    for i = 0에서 마지막까지
    현재 남은 시간 체크 
    현재 남은시간 == 0:
        현재 machine상태 = available
        남은 시간 = 0인 machine들 체크 
    
    for i in 남은시간=0인machine:
        다음 Machine == available인지 확인
"""



## ---------  Test Area ------------------------------------------------------------------------------------------------------------------------------
def main():
## Create Environment
    Env = Environment()

## Run Environment
    Env.run()
    print(Env.process[0].leadTime)
    print(Env.process[0].available)
    



if __name__ == '__main__':
    main()




## -------- Explanation & references  ---------------------------------------------------------------------------------------------------------
"""

class Test():
    def __init__(self):
        self.num = randint(0,100)
    
    def show(self) :
        print(self.num)

"""
