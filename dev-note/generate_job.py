import random
from statistics import mean

job = []
mc1_proc = []
mc2_proc = []

# machine1의 process time 생성.
for _ in range(0,10):
    mc1_proc.append(random.randint(20,30))
    mc2_proc.append(random.randint(10, 20))


print('-'*20 + 'process time for machine 1' + '-'*20)
for i in range(0,10):
    print(mc1_proc[i])
print(f'average for machine1 proc time = {mean(mc1_proc)}')

print('\n'*3)

print('-'*20 + 'process time for machine 2' + '-'*20)
for i in range(0,10):
    print(mc2_proc[i])
print(f'average for machine2 proc time = {mean(mc2_proc)}')


for pair in zip(mc1_proc, mc2_proc):
    job.append(pair)

ct = 1
for i in job:
    print(f'{ct}번째 job : {i}\n')
    ct += 1