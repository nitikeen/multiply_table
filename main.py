import random
from datetime import datetime
import time
import json

def level(stat):
    result = 9
    for a in stat['mul']:
        total = 0
        for b in stat['mul'][a]:
            total += stat['mul'][a][b]
            if stat['mul'][a][b] > 30 and result > int(a):
                result = int(a)
        dev = total / len(stat['mul'][a])
    for a in stat['dev']:
        total_dev = dict()
        for b in stat['dev'][a]:
            # total_dev[b] += stat['dev'][a][b]
            if stat['dev'][a][b] > 30 and result > int(b):
                result = int(b)
    return result


op = ('mul', 'dev')

print('Тренажер таблицы умножения и деления')
try:  # Открываем файл со статистикой
    with open("stat.json", "r") as read_file:
        stat = json.load(read_file)
except IOError:
    stat = dict()
current_level = level(stat)
start_level = 0
while True:  # Повторяем опрос
    if start_level != current_level:
        print(f'Вы на уровне {current_level}')
        start_level = current_level
    while True:  # Генерируем задачу
        operation = random.choice(op)
        if operation == 'mul':  # Умножение
            a = random.randint(1, current_level)
            b = random.randint(1, 9)
            fx = f'{a} x {b}'
            result = a * b
        else:  # Деление
            b = random.randint(1, current_level)
            a = b * random.randint(1, 9)
            fx = f'{a} : {b}'
            result = a / b
        # Проверяем, что данная задача есть в статистике, если нет - добавляем
        if operation not in stat:
            stat[operation] = dict()
        if str(a) not in stat[operation]:
            stat[operation][str(a)] = dict()
        if str(b) not in stat[operation][str(a)]:
            stat[operation][str(a)][str(b)] = 100
        stat_duration = stat[operation][str(a)][str(b)]
        # Чем лучше статистика по задаче, тем реже утверждаем эту задачу
        if random.randint(0, 100) <= stat_duration:
            break  # Утвердили задачу
    while True:  # Запрашиваем ответ
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
                time.sleep(2)
            # Обновляем статистику
            stat[operation][str(a)][str(b)] = (stat[operation][str(a)][str(b)] + answer_duration) / 2
            with open("stat.json", "w") as write_file:
                json.dump(stat, write_file, indent=4, sort_keys=True)
            time.sleep(2)
            current_level = level(stat)
            break
