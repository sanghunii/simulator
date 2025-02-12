import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from collections import deque

# 1️⃣ 환경 정의 (Scheduling Environment)
class SchedulingEnv:
    def __init__(self, num_jobs=20):
        self.num_jobs = num_jobs
        self.reset()

    def reset(self):
        """환경 초기화: 20개의 작업을 생성하고 초기 확률을 설정"""
        self.jobs = [{"id": i, "processing_time": random.randint(1, 10),
                      "inspection_prob": 0.5} for i in range(self.num_jobs)]
        self.current_time = 0  # 현재 시간
        return self.get_state()  # 초기 상태 반환

    def step(self, action):
        """DQN이 선택한 작업(action)에 따라 환경을 업데이트"""
        selected_job_id = action // 2  # 선택된 작업 ID
        performed_inspection = (action % 2) == 1  # 0이면 검사 X, 1이면 검사 O

        # 선택된 작업 정보 가져오기
        selected_job = self.jobs[selected_job_id]
        self.current_time += selected_job["processing_time"]  # 작업 수행 → 시간 업데이트


        # 검사 수행 여부에 따른 추가 보상 또는 패널티
        if performed_inspection:
            reward -= 5  # 검사 비용 패널티
            reward += 5 if random.random() < selected_job["inspection_prob"] else -5  # 품질 향상 보상

        # 작업 완료 → 리스트에서 제거
        self.jobs.remove(selected_job)

        # 다음 작업의 `inspection_prob` 업데이트
        for job in self.jobs:
            if performed_inspection:
                job["inspection_prob"] = min(1.0, job["inspection_prob"] * 1.2)  # 확률 증가
            else:
                job["inspection_prob"] = max(0.0, job["inspection_prob"] * 0.8)  # 확률 감소

        # 종료 여부 확인
        done = len(self.jobs) == 0

        return self.get_state(), reward, done  # 다음 상태, 보상, 종료 여부 반환

    def get_state(self):
        """현재 남은 작업 리스트를 고정된 길이(20)로 변환하여 반환"""
        state = []
        for job in self.jobs:
            state.append([job["processing_time"], job["inspection_prob"]])
        
        # 작업이 20개 미만이면, 더미 값(0) 추가하여 고정 길이 유지
        while len(state) < 20:
            state.append([0, 0])

        return np.array(state).flatten()  # 1D 벡터로 반환

# 2️⃣ DQN 에이전트 정의
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # 할인율
        self.epsilon = 1.0  # 초기 탐색 확률
        self.epsilon_min = 0.01  # 최소 탐색 확률
        self.epsilon_decay = 0.995  # 탐색 감소율
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        """DQN 모델 정의"""
        model = Sequential([
            Dense(64, input_dim=self.state_size, activation="relu"),
            Dense(64, activation="relu"),
            Dense(self.action_size, activation="linear")  # 40개의 행동(Action) Q-value 출력
        ])
        model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        """경험 저장"""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """현재 상태에서 행동(Action) 선택"""
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)  # 탐색 (랜덤 행동)
        q_values = self.model.predict(state.reshape(1, -1))
        return np.argmax(q_values[0])  # 최적 행동 선택

    def train(self, batch_size=32):
        """Experience Replay를 사용하여 학습"""
        if len(self.memory) < batch_size:
            return  # 메모리가 충분하지 않으면 학습하지 않음
        
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.max(self.model.predict(next_state.reshape(1, -1))[0])
            
            target_f = self.model.predict(state.reshape(1, -1))
            target_f[0][action] = target
            self.model.fit(state.reshape(1, -1), target_f, epochs=1, verbose=0)

        # Epsilon 감소 (탐색 비율 점진적 감소)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# 3️⃣ 메인 학습 루프
env = SchedulingEnv()
state_size = len(env.get_state())  # 20개 job * 4개 feature = 80차원
action_size = 40  # 20개 작업 × 2개 검사 여부
agent = DQNAgent(state_size, action_size)

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0

    for step in range(20):  # 최대 20개의 작업
        action = agent.act(state)  # 행동 선택
        next_state, reward, done = env.step(action)  # 환경 업데이트
        agent.remember(state, action, reward, next_state, done)  # 경험 저장
        state = next_state  # 상태 업데이트
        total_reward += reward

        if done:
            break  # 모든 작업이 끝나면 종료

    agent.train(batch_size=32)  # 학습
    print(f"Episode {episode + 1}: Total Reward = {total_reward}")

print("Training Complete!")
