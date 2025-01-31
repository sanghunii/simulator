import pandas as pd
import random 
from typing import List, Dict


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








# Simulate - NonPermutation (Create and Fill up Report)
def Simulate_Nonpermutation(
        RL_result: Dict[str, List] = None,
        #report: pd.DataFrame = None,
        report = None,
        job_num: int = None,
        machine_num: int = None,
        mc_job_matrix: List[List[int]] = None,
        inspect_point: int = None,
        inspect_proc: int = None,
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