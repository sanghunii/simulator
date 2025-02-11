# import functinos
from module.common import make_job_proc_time, CreateReportOutline
from module.permutation import Scheduling_Permutation, Simulate_Permutation
from module.non_permutation import Scheduling_NPermutation, Simulate_Nonpermutation

# import constants
from module.common import job_num, inspect_point, inspect_proc, machine_range, machine_num

# typehint
from typing import Dict, List

import pandas as pd


class ENV():
    def __init__(
            self,
            job_num: int = job_num,
            inspect_point: int = inspect_point,
            inspect_proc: int = inspect_proc,
            machine_num: int = machine_num,
            machine_range: List[List[int]] = machine_range
    ):
        self.job_num = job_num
        self.inspect_point = inspect_point
        self.inspect_proc = inspect_proc
        self.machine_num = machine_num
        self.machine_range = machine_range
        self.mc_job_matrix = None
        self.RL_result = None
        self.report = None
        """self.report:
            Permutation이라면 pd.DataFrame
            Non_permutation이라면 List[pd.DataFrame]"""


##Permutation Simulation Method
    def Run_Permutaion(self) -> pd.DataFrame:
        # Get mc_job_matrix
        self.mc_job_matrix = make_job_proc_time(
            machine_num=self.machine_num,
            job_num = self.job_num,
            machine_range=self.machine_range
        )

        # Shceduling 
        # *******Use ReinformentLearning Model For this part*********
        self.RL_result = Scheduling_Permutation(
            job_num=self.job_num,
            mc_job_matrix=self.mc_job_matrix
        )

        # Create Inital Report 
        self.report = CreateReportOutline(
            RL_result=self.RL_result,
            machine_num=self.machine_num
        )

        # Complete Report 
        self.report = Simulate_Permutation(
            RL_result=self.RL_result,
            report=self.report,
            job_num=self.job_num,
            machine_num=self.machine_num,
            mc_job_matrix=self.mc_job_matrix,
            inspect_point=self.inspect_point,
            inspect_proc=self.inspect_proc
        )

        return self.report
    
##NonPermutation Simulation Method
    def Run_Nonpermutation(self) -> List[pd.DataFrame]:
        # Get mc_job_matrix
        self.mc_job_matrix = make_job_proc_time(
            machine_num=self.machine_num,
            job_num=self.job_num,
            machine_range=self.machine_range
        )

        # Shceduling 
        # *******Use ReinformentLearning Model For this part*********
        self.RL_result = Scheduling_NPermutation(
            job_num=self.job_num,
            mc_job_matrix=self.mc_job_matrix
        )
        
        # Create Initial Report
        self.report = CreateReportOutline(
            RL_result=self.RL_result,
            machine_num=self.machine_num
        )

        self.report = Simulate_Nonpermutation(
            RL_result=self.RL_result,
            report=self.report,
            job_num = self.job_num,
            machine_num=self.machine_num,
            mc_job_matrix=self.mc_job_matrix,
            inspect_point=self.inspect_point,
            inspect_proc=self.inspect_proc
        )

        return self.report
    
    def show(self):
        print(self.RL_result)


        
        
        




"""Test Code"""
def main():
    env = ENV()
    reports = env.Run_Nonpermutation()
    env.show()
    
    
    

if __name__ == '__main__':
    main()