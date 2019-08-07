GYM_ENVIROMENT = "MountainCar-v0"
LEARNING_RATE = 0.1
DISCOUNT = 0.99
EPISODES = 20_000
SHOW_EVERY = 2_000
DISCRETE_SIZE = 20
EPSILON = 1
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES // 2
EPSILON_DECAY_VALUE = EPSILON / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

REPLAY_MEMORY_SIZE = 50_000
DEEP_EPISODES = 10_000
MIN_REPLAY_MEMORY_SIZE = 1_000
MINIBATCH_SIZE = 16
UPDATE_TARGET_EVERY = 5
AGGREGATE_STATS_EVERY = 500
MIN_EPSILON = 0.001
MIN_REWARD = -200
MODEL_NAME = 'DeepQLearning'
