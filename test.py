
import random

confs = [1, 0, 2, 1, 0, 2, 1, 1, 1, 0]




min_conf = min(confs)
rand_min = random.choice([i for i in range(len(confs)) if confs[i] == min_conf])

print(rand_min)