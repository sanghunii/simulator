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
        for i in range(0, operatingNum):
            self.leadTimes.append(randint(10,30))
        
    
    def showLeadTime(self):
        for i in range(0, self.operatingNum):
            print('-------------------')
            print(f"{i +1}번째 machine lead time : ", self.leadTimes[i])
            
        


    
 


class Machine():
    def __init__(
            self,
            leadTime: int| float = 1,   ##given by Job
            Mode: bool = False, ##False means permutation / True means nonPermutation
            inspection: bool = False,   ##True면 해당 machine은 inspection을 담당하는 machine.
            available: bool = True,     ##True면 해당 machine은 현재 job을 받을 수 있는 상태
    ):
        self.leadTime: int| float = leadTime
        self.inspection: bool = inspection


class Environment():
    def __init__(
            self,
            Mode: bool = False, ##False means permutation / True means nonPermutation
            machineNum: int = 1, ##해당 갯수만큼의 Machine List를 만듦
            jobNum: int = 5 ##해당 갯수만큼의 Job List를 만듦.
    ):
        self.Mode = Mode
        self.machineNum = machineNum
        self.makespan=0 ##전체 Process소요시간




## ---------  Test Area ------------------------------------------------------------------------------------------------------------------------------
def main():
## Creat Job Process
    jobTest = Job()

##Show Created Jobs
    jobTest.showLeadTime()
        





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
