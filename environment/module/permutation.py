import pandas as pd
import random 
from typing import List, Dict


### shceduling_Permutaiton with ReinforcementLearning
def Scheduling_Permutation(
        job_num: int = None,
        mc_job_matrix: List[List[int]] = None
) -> Dict[str, List] :
    
    if (job_num == None):
        raise Exception("job_num이 입력되지 않았습니다.")
    
    x=0
    job_sequence = []

    for _ in range(job_num):
        job_sequence.append(x)
        x+=1
    
    
    ##Permutation상황에서는 JobSequence의 순서가 바뀌지 않으므로 mc0_job_sequence만 있으면 된다.
    RL_result = {
        "job_inspection": None,
        "mc0_job_sequence": job_sequence,
    }

    # scheduling
    random.shuffle(job_sequence)

    # inspection 대상 생성 코드
    job_inspection = []
    inspection = random.randint(0,5)

    for _ in range(job_num):
        if _ == inspection:
            job_inspection.append(1)
        else:
            job_inspection.append(0)
    
    RL_result['job_inspection'] = job_inspection
    RL_result['mc0_job_sequence'] = job_sequence
    
    
    return RL_result





# Simulate - Permutation (Create and Fill up Report)
def Simulate_Permutation(
        RL_result: Dict[str, List] = None,
        report = None,
        job_num: int = None,
        machine_num: int = None,
        mc_job_matrix: List[List[int]] = None,
        inspect_point = None,
        inspect_proc = None
) -> pd.DataFrame:  
    

    
    if RL_result == None:
        raise Exception("RL_result가 입력되지 않았습니다.")
    """if report == None:
        raise Exception("report가 입력되지 않았습니다.")"""
    if machine_num == None:
        raise Exception("machine_num이 입력되지 않았습니다.")
    if mc_job_matrix == None:
        raise Exception("mc_job_matrix가 입력되지 않았습니다.")

    total_proc_num = machine_num*2 + 2 # 총 공정 수

    for seq in range(0, job_num):
        for mc in range(3, 3 + total_proc_num):
            
            # inspect in 칼럼 검토 중인 경우 
            ## inspect point = 2면 2개의 machine을 거친다음 inspection진행
            ## 모든 Machined의 i/o를 고려하므로 report상에서의 inspect_input
            if mc == (3 + inspect_point*2):
                if seq == 0: # 첫 번째 작업은 예외 처리
                    report.iloc[0, mc] = report.iloc[0, mc-1]
                else:
                    report.iloc[seq, mc] = max(report.iloc[seq, mc-1], report.iloc[seq-1, mc+1])
                    
            # inspect out 칼럼 검토 중인 경우
            elif mc == (3 + inspect_point*2 + 1):
                if report.iloc[seq, 1] == 1: # inspection 대상인 경우
                    report.iloc[seq, mc] = report.iloc[seq, mc-1] + inspect_proc
                else:
                    report.iloc[seq, mc] = report.iloc[seq, mc-1] # 아닌 경우
                                        
            # 일반 기계 in 칼럼 검토 중인 경우
            elif mc % 2 == 1: #기계의 in인 경우
                if seq == 0: # 첫 번째 작업은 예외 처리
                    report.iloc[0, mc] = report.iloc[0, mc-1]
                else: 
                    report.iloc[seq, mc] = max(report.iloc[seq, mc-1], report.iloc[seq-1, mc+1])
            
            # 일반 기계 out 칼럼 검토 중인 경우
            else: 
                col = report.columns[mc]   
                machine = int(col[2:3])
                job = report.iloc[seq, 0]
                report.iloc[seq, mc] = report.iloc[seq, mc-1] + mc_job_matrix[machine][job]
                
    ret_report = report.drop(columns = 'temp')
    ret_report

    return report