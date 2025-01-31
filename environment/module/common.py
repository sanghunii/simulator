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