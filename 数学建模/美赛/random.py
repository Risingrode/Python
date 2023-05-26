import random

# 生成 10 个在 1-20000 区间内的随机整数
random_numbers = [random.randint(1, 20000) for _ in range(10)]
random_numbers.sort()

# 分组
group_size = len(random_numbers) // 10
groups = [random_numbers[i:i+group_size] for i in range(0, len(random_numbers), group_size)]

print(groups)