import random

level = {}
base_exp = 50

for i in range(1, 101):
    if i == 1:
        level[str(i)] = {'exp': base_exp}
    else:
        prev_exp = level[str(i - 1)]['exp']
        new_exp = int(prev_exp * random.uniform(1.10, 1.15))
        level[str(i)] = {'exp': new_exp}
