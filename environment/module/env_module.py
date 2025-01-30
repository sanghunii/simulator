import numpy as np
import pandas as pd
import random 
from typing import List, Dict

# job (변경 가능)
job_num = 5

# inspect (변경 가능)
inspect_proc = 30 
inspect_point = 1

# machine (변경 가능)
mc1_range = [10,20]
mc2_range = [20,30]
machine_range = [mc1_range, mc2_range]
machine_num = len(machine_range)





## Create Job For Input
def make_job_proc_time( 
        machine_num: int = None, 
        job_num: int = None, 
        machine_range: List[List[int]] = None 
) -> List[List[int]]:
    
    if machine_num == None:
        raise Exception("machine_num이 입력되지 않았습니다.")
    if job_num == None:
        raise Exception("job_num이 입력되지 않았습니다.")
    if machine_range == None:
        raise Exception("machine range가 입력되지 않았습니다.")
    
    mc_job_matrix = []
    for i in range(machine_num):
        job_proc = []
        for _ in range(job_num):
            job_proc.append(random.randint(machine_range[i][0], machine_range[i][1]))
        mc_job_matrix.append(job_proc)
    
    return mc_job_matrix




# Shceduling Nonpermutation with ReinforcementLearning
# 일단 임시 모듈을 만들어서 사용한다.
# 개발 된 RL모듈은 이 부분에 import된다. 
# RL agent는 각 machine별로 job 투입 순서를 정한다.
def Scheduling_NPermutation (
        job_num: int = None,
        mc_job_matrix: List[List[int]] = None  ##나중에 사용할 RL module은 이 mc_job_matrix를 보고 job scheduling을 진행한다. 
) -> Dict[str, List] :
    
    ##이후 해당 코드 Decorator로 만들기
    if (job_num == None):
        raise Exception("job_num이 입력되지 않았습니다.")
    
    ##해당 부분 globals이용해서 동적인 코드로 변환 해야함.
    mc0_job_sequence = []
    mc1_job_sequence = []
    RL_result = {
        "mc0_job_sequence": mc0_job_sequence,
        "mc1_job_sequence": mc1_job_sequence,
        "job_inspection": None
    }

    # create job_seqence
    x = 0
    job_sequence = []

    """아래 코드들은 임시 Create Job Sequene Code
                RL module이 이자리에 들어가서 Scheudling을 한다."""
    
    # SchedulingPart(이 부분에 RL Module 삽입) 
    for _ in range(job_num):
        job_sequence.append(x)
        x+=1

    # machine별 job_sequence(job투입순서)
    random.shuffle(job_sequence)
    mc0_job_sequence = job_sequence[:]

    random.shuffle(job_sequence)
    mc1_job_sequence = job_sequence[:]

    # inspection 대상 생성 코드 (한개만 한다고 가정)
    job_inspection = []
    inspection = random.randint(0,5)

    for _ in range(job_num):
        if _ == inspection:
            job_inspection.append(1)
        else:
            job_inspection.append(0)

    
    RL_result['job_inspection'] = job_inspection
    RL_result['mc0_job_sequence'] = mc0_job_sequence
    RL_result['mc1_job_sequence'] = mc1_job_sequence
    
    return RL_result




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


def CreateReportOutline( 
        RL_result: Dict[str, int] = None,
        machine_num: int = None
) -> pd.DataFrame:
    """스케쥴링 결과를 받아서 report outline을 생성한다."""

    if RL_result == None:
        raise Exception("RL_result가 입력되지 않음")
    if machine_num == None:
        raise Exception("machine_num이 입력되지 않음")
    
    report = pd.DataFrame({
        'job': RL_result.get('mc0_job_sequence'),
        'inspect': RL_result.get('job_inspection')
    })

    report['temp'] = 0

    col_list = [[f'mc{i}i', f'mc{i}o'] for i in range(machine_num)]
    concat = ['insi', 'inso']

    col_list.insert(inspect_point, concat)
    
    col_list = [item for temp in col_list for item in temp]

    report[col_list] = None
    
    return report


# Simulate - NonPermutation (Create and Fill up Report)
def Simulate_Nonpermutation(
        RL_result: Dict[str, List] = None,
        #report: pd.DataFrame = None,
        report = None,
        machine_num: int = None,
        mc_job_matrix: List[List[int]] = None
        ) -> List[pd.DataFrame]:
    
    if (RL_result == None):
        raise Exception("RL_reuslt이 입력되지 않음")
    """if (report == None):
        raise Exception("report가 입력되지 않았습니다.")"""
    if (machine_num == None):
        raise Exception("machine_num이 입력되지 않음")
    if (mc_job_matrix == None):
        raise Exception("mc_job_matrix가 입력되지 않음")
    
    
    ret_reports = []
    
    

    
    """Ver. NonPermutation"""
    """Step1.  (1st machine - inspection process)"""
    total_proc_num = machine_num * 2  + 2 
    print(f"total proc num = {machine_num * 2 + 2}")

    for seq in range(0, job_num):
        for mc in range(3, 3 + inspect_point*2 + 2):
            
            # inspect in column 검터 중인 경우
            if mc == (3 + inspect_point*2):
                ##첫 번째 작업일 경우 예외처리
                if seq == 0:
                    report.iloc[0, mc] = report.iloc[0, mc-1]
                # 첫 번째 작업이 아니라면 
                else:
                    ##inspect 대상일 경우
                    if report.loc[seq, 'inspect'] == 1:
                        previous_insp = -1
                        previous_ins_seq = -1

                        # 이전에 insepction을 거친 job이 있는지 탐색
                        # 있다면 그 job의 inpsection out타임과 지금 job의 이전 machine의 output time을 비교해서 더 큰값을 insi로 집어넣는다.
                        pre_porc = range(0, seq)
                        for i in reversed(range(0, seq)):
                            previous_insp = report.loc[i,'inspect']
                            if (previous_insp == 1):
                                previous_ins_seq = i
                                break
                        # 지금이 처음이라면
                        if (previous_insp == 0):
                            report.iloc[seq, mc] = report.iloc[seq, mc-1]

                        # 이전 단계에 inspection을 거친 job이 있다면 
                        else:
                            report.iloc[seq, mc] = max(report.iloc[seq, mc-1], report.iloc[previous_ins_seq, mc+1])
                    # inspection 대상이 아닐경우 
                    else:
                        report.iloc[seq, mc] = report.iloc[seq, mc-1]

            # inspect out칼럼 검터 중인 경우
            elif mc == (3 + inspect_point*2 + 1):
                # insepct 대상 O
                if report.loc[seq, 'inspect'] == 1:
                    report.iloc[seq, mc] = report.iloc[seq, mc-1] + inspect_proc
                
                # insepct 대상 X
                else:
                    report.iloc[seq, mc] = report.iloc[seq, mc-1]
            

            # 일반 기계 in 칼럼 검토 중인 경우
            elif mc % 2 == 1:
                # 첫번째 작업 예외
                if seq == 0:
                    report.iloc[0, mc] = report.iloc[0, mc-1]
                else:
                    report.iloc[seq, mc] = max(report.iloc[seq, mc-1], report.iloc[seq-1, mc+1])
            
            # 일반 기계 out 칼럼 검토 중인 경우
            else:
                col = report.columns[mc]
                machine = int(col[2:3])
                job = report.iloc[seq, 0]
                report.iloc[seq, mc] = report.iloc[seq, mc-1] + mc_job_matrix[machine][job]

    print(f"mc0_job_input_order : {RL_result.get("mc0_job_sequence")}\n")
    ret_reports.append(report)


    """step2. machine2"""
    report = report.set_index('job').reindex(RL_result.get('mc1_job_sequence'))
    report = report.reset_index(drop=False)

    for seq in range(0, job_num):
        for mc in range(3 + inspect_point * 2 + 1  + 1, 3 + total_proc_num):
            
            # 일반 Mahcine Input
            if mc % 2 == 1:
                # 첫번째 작업 예외 처리
                if seq == 0:
                    report.iloc[seq, mc] = report.iloc[seq, mc-1]
                else:
                    report.iloc[seq, mc] = max(report.iloc[seq, mc-1], report.iloc[seq-1, mc+1])

            # 일반 Machine Output
            else:
                col = report.columns[mc]
                # machine number parsing
                macine = int(col[2:3])
                # job number parsing
                job = report.iloc[seq, 0]
                report.iloc[seq, mc] = report.iloc[seq, mc-1] + mc_job_matrix[machine][job]
    
    ret_reports.append(report)
    
    return ret_reports
                    



# Simulate - Permutation (Create and Fill up Report)
def Simulate_Permutation(
        RL_result: Dict[str, List] = None,
        report = None,
        machine_num: int = None,
        mc_job_matrix: List[List[int]] = None
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




def main():
    """1. Test None Permutation functions"""
    ## 1. create machine_job_matrix 
    mc_job_matrix = make_job_proc_time(job_num=job_num, machine_num=machine_num, machine_range=machine_range)
    print(mc_job_matrix)

    ## 2. Scheduing
    RL_result = Scheduling_Permutation(job_num=job_num)
    print(RL_result)

    ## 3. Create Initial Report
    report = CreateReportOutline(RL_result=RL_result, machine_num=machine_num)
    print(report)

    ## 4. Simulate
    reports = Simulate_Permutation(RL_result=RL_result, report=report, machine_num=machine_num, mc_job_matrix=mc_job_matrix)
    print(reports)
    
    

if __name__ == "__main__":
    main()