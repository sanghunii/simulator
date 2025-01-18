import pandas as pd
import numpy as np

import random



# input: job_num, inspect_itv, inspect_proc, machine_proc_range

job_num = 5 #### 
inspect_itv = 2
inspect_proc = 30
machine_range = [[10, 20], [20, 30], [10, 50]]

# input 바탕으로 변수 생성
machine_num = len(machine_range)
inspect_point = random.randint(0, machine_num)  # 실제론 이렇게 쓰겠지만, 코드를 위해 상수 고정 후 코딩
#inspect_point = 2 # 2 번째 기계 완료 후 검사 진행


# 기계의 작업 시간 범위에 맞춰서 작업 시간 생성
def make_job_proc_time(machine_num, job_num, machine_range):
    mc_job_matrix = []
    for i in range(machine_num):
        jobs_proc = []
        for j in range(job_num):
            jobs_proc.append(random.randint(machine_range[i][0], machine_range[i][1]))
        mc_job_matrix.append(jobs_proc)
    return mc_job_matrix

print(f"inspection point = {inspect_point}")


# 실행
mc_job_matrix = make_job_proc_time(machine_num, job_num, machine_range)
mc_job_matrix



# RL 결과 대신 랜덤값으로 대체
## job_sequence 생성 코드
x=0
job_sequence = []

for _ in range(job_num):
    job_sequence.append(x)
    x+=1

random.shuffle(job_sequence)
job_sequence

## inpection 대상 생성 코드
job_inspection = []
for _ in range(job_num):
    job_inspection.append(random.randint(0,1))
    
    
RL_result = [job_sequence, job_inspection]
RL_result


# 레포트 데이터 프레임 생성
# 레포트 기초 정보 칼럼 생성
report = pd.DataFrame({'job':RL_result[0],
                             'inspect':RL_result[1]})

# 계산을 위해 임시 피쳐 생성
report['temp'] = 0


# 기계, 검사 정보 칼럼 생성
col_list = [[f'mc{i}i', f'mc{i}o'] for i in range(machine_num)]
concat = ['insi', 'inso']

col_list.insert(inspect_point, concat)
print(f"col_list : {col_list}")

# 리스트 평면화
col_list = [item for temp in col_list for item in temp]

# 칼럼 합치기
report[col_list] = None
report




### Ver. 2 - NonPermutation
total_proc_num = machine_num*2 + 2 #총 공정 수 = machine * 2 (I/O) + 2(inpect I/O)

for seq in range(0, inspect_point + 1): ##inspect Output지점까지 일단 숫자 다채움
    for mc in range(3, 3 + total_proc_num):


        ##inspect in column 검토 중인 경우
        if mc == (3 + inspect_point*2):

        ##첫 번째 작업일 경우 예외처리
            if seq == 0:
                report.iloc[0, mc] = report.iloc[0,mc-1]
            else:
                previous_inspec = -1
                previous_ins_seq = -1
                """
                이전 inspect를 거친 job을 찾는다.
                그 job의 inpect output과 지금 내 job의 이전 out을 비교해 더 큰값을 inpect input값으로 한다.
                """
                pre_proc = range(0, seq)
                for i in reversed(pre_proc):
                    previous_inspec = report.iloc[i,1]
                    if previous_inspec is 1:
                        previous_ins_seq = pre_proc
                        break
                ##지금 inpect가 처음 이라면
                if previous_inspec is 0: 
                    report.iloc[seq, mc] = report.iloc[seq, mc-1]

                ##이전 단계에 inspect가 들어간 Job이 있다면
                ##젤 최근에 inspect를 진행한 Job의 InspectOutput과 현재 job의 이전 단계 machine의 output중에서 큰 값을 집어넣는다.
                else:
                    report.iloc[seq, mc] = max(report.iloc[seq, mc-1], report.iloc[previous_ins_seq, mc+1]) 
        
        
            ##inspect out칼럼 검토 중인 경우
            if mc == (3 + inspect_point*2 + 1):
            ## inspect대상일 경우
                if report.iloc[seq,1] == 1:
                    report.iloc[seq,mc] = report.iloc[seq,mc-1] + inspect_proc
            ## inspect대상이 아닐 경우
                else:
                    report.iloc[seq, mc] = report.iloc[seq,mc-1] 
                    
        
                    
                    
                
                


"""
#### Ver.1 - Permutation
total_proc_num = machine_num*2 + 2 # 총 공정 수

for seq in range(0, job_num):
    print(seq)
    for mc in range(3, 3 + total_proc_num):
        print(mc)
        print(f'{seq}번째 순서 작업의 {report.columns[mc]}')
        
        # inspect in 칼럼 검토 중인 경우 
        ## inspect point = 2면 2개의 machine을 거친다음 inspection진행
        ## 모든 Machined의 i/o를 고려하므로 report상에서의 inpsect_input
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
    
        # 일반 기계 out 칼럼 검토 중인 경우.
        else: 
            col = report.columns[mc]    ##몇 번째 machine인지 parsing
            machine = int(col[2:3])     ##machine 숫자 parsing - 2번째 machine이면 2가 들어가겠지? 
            job = report.iloc[seq, 0]   ##현재 job번호를 parsing
            report.iloc[seq, mc] = report.iloc[seq, mc-1] + mc_job_matrix[machine][job] 
            ##mc_job_matrix에서 job의 해당 machine에서의 leadTime을 가져와서 input시점에다가 더해준다. 그 값이 output시점이다.
            
final_report = report.drop(columns = 'temp')

print(mc_job_matrix)
print(final_report)
"""