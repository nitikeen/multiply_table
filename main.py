import random
from datetime import datetime
import time
import json

op = ('mul', 'dev')

stat = dict(mul={a + 1: {b + 1: 100 for b in range(9)} for a in range(9)},
            dev={a + 1: {b + 1: 100 for b in range(9)} for a in range(81)})
print(stat)
print('Тренажер таблицы умножения и деления')
while True:  # Повторяем опрос
    while True:  # Генерируем задачу
        b = random.randint(1, 9)
        operation = random.choice(op)
        if operation == 'mul':
            a = random.randint(1, 9)
            fx = f'{a} x {b}'
            result = a * b
        else:
            a = b * random.randint(1, 9)
            fx = f'{a} : {b}'
            result = a / b
        if random.randint(0, 100) <= stat[operation][a][b]:
            break
    while True:
        try:
            start_time = datetime.now()
            answer = int(input(f'{fx} = '))
        except ValueError:
            print('Введите число')
        else:
            if answer == result:
                time_elapsed = datetime.now() - start_time
                print(f'Верно! ({round(time_elapsed.total_seconds())} сек)')
                answer_duration = time_elapsed.total_seconds()
            else:
                print(f'Не верно, {round(result)}')
                answer_duration = 100
            stat[operation][a][b] = (stat[operation][a][b] + answer_duration) / 2
            print(stat)
            time.sleep(2)
            break
