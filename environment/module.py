##강화학습 Enviornment 구성하는 class모음
"""
1. JobClass
    각 Job
2. MachineClass (Job)
"""

from typing import List, Optional
from random import randint

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
            machineNum: int = 0,
            leadTime: int| float = 0,   ##given by Job
            mode: bool = False, ##False means permutation / True means nonPermutation
            inspection: bool = False,   ##True면 해당 machine은 inspection을 담당하는 machine.
            available: bool = True,     ##True면 해당 machine은 현재 job을 받을 수 있는 상태 
    ):
    ##set attributes 
        self.job = job
        self.machineNum = machineNum
        self.leadTime = leadTime
        self.mode = mode
        self.inspection = inspection
        self.available = available
    

##Job을 할당할때 setMachine을 이용해서 Machine을 세팅한다.
    def setMachine(
            self,
            job: Job,
            leadTime: int,
    ):
        self.job = job
        self.leadTime = job.getLeadtime(machineNum = self.machineNum)
        self.available = False
    
    
    




class Environment():
    def __init__(
            self,
            Mode: bool = False, ##False means permutation / True means nonPermutation
            machineNum: int = 1, ##해당 갯수만큼의 Machine List를 만듦
            jobNum: int = 5 ##해당 갯수만큼의 Job List를 만듦.
    ):
        self.Mode: bool = Mode
        self.machineNum: int = machineNum
        self.makespan:int = 0  ##전체 Process소요시간
        self.jobPool: List[Job]





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
## Creat Job Process
    job = Job()

## Test job method
    for i in range(0,10):
        leadTime = job.getLeadTime(i)
        print('-------------------')
        print(f"{i}번째 machine lead time : ", leadTime)
    



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
