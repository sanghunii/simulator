# import functinos
from module import env_module 

# typehint
from typing import Dict, List

import pandas as pd


class ENV():
    def __init__(
            self,
            job_num: int = env_module.job_num,
            machine_num: int = env_module.machine_num,
            machine_range: List[List[int]] = env_module.machine_range
    ):
        self.job_num = job_num
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
        self.mc_job_matrix = env_module.make_job_proc_time(
            machine_num=self.machine_num,
            job_num = self.job_num,
            machine_range=self.machine_range
        )

        # Shceduling 
        # *******Use ReinformentLearning Model For this part*********
        self.RL_result = env_module.Scheduling_Permutation(
            job_num=self.job_num,
            mc_job_matrix=self.mc_job_matrix
        )

        # Create Inital Report 
        self.report = env_module.CreateReportOutline(
            RL_result=self.RL_result,
            machine_num=self.machine_num
        )

        # Complete Report 
        self.report = env_module.Simulate_Permutation(
            RL_result=self.RL_result,
            report=self.report,
            machine_num=self.machine_num,
            mc_job_matrix=self.mc_job_matrix
        )

        return self.report
    
##NonPermutation Simulation Method
    def Run_Nonpermutation(self) -> List[pd.DataFrame]:
        # Get mc_job_matrix
        self.mc_job_matrix = env_module.make_job_proc_time(
            machine_num=self.machine_num,
            job_num=self.job_num,
            machine_range=self.machine_range
        )

        # Shceduling 
        # *******Use ReinformentLearning Model For this part*********
        self.RL_result = env_module.Scheduling_NPermutation(
            job_num=self.job_num,
            mc_job_matrix=self.mc_job_matrix
        )
        
        # Create Initial Report
        self.report = env_module.CreateReportOutline(
            RL_result=self.RL_result,
            machine_num=self.machine_num
        )

        self.report = env_module.Simulate_Nonpermutation(
            RL_result=self.RL_result,
            report=self.report,
            machine_num=self.machine_num,
            mc_job_matrix=self.mc_job_matrix
        )

        return self.report


        
        
        




"""Test Code"""
def main():
    
    env = ENV()
    report = env.Run_Nonpermutation()
    print(report[0])
    print(report[1])
    

if __name__ == '__main__':
    main()