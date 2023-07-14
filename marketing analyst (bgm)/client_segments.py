import csv


def date_change(d: tuple) -> int:
    """На вход поступает кортеж с 3мя числами, соответствующими дате, месяцу и году.
    Функция вычисляет диапазон между введённой датой и 01.01.2023г в месяцах,
    и возвращает это значение целым числом. Неполные месяцы округляются в большую сторону.
    Смысл выходного числа: в диапазон какого по счёту из ближайших месяцев от даты 01.01.2023 входит дата чека"""
    res = (2023 - d[2]) * 12 + (1 - d[1])  # число нам не важно, только разница в месяцах,
    # поскольку мы отсчитываем в прошлое от 1 января
    return res


with open('Исходные данные.txt', encoding="utf-8") as file:
    transactions_2Dlist = [s.strip().split() for s in
                           file.readlines()]  # формируем список списков на основе входных строк

clients = {}  # инициализация словаря клиентов с Guid в качестве ключа и списком дат в качестве значений
cheks_by_months = {}

for transaction in transactions_2Dlist[1:]:  # проходим список транзакций и на их основе создаём словарь, где
    # ключ - Guid клиента, а значение - список дат всех чеков этого клиента
    d = tuple(map(int, transaction[0].split('.')))  # кортеж с числовыми значениями числа, месяца и года из даты
    if transaction[2] in clients:
        clients[transaction[2]].append(d)
    else:
        clients[transaction[2]] = [d]
    # а также параллельно вычисляем количество чеков по месяцам/годам, чтобы 2 раза не проходить по чекам
    if d[2] in cheks_by_months:
        if d[1] in cheks_by_months[d[2]]:
            cheks_by_months[d[2]][d[1]] += 1
        else:
            cheks_by_months[d[2]][d[1]] = 1
    else:
        cheks_by_months[d[2]] = {}
        cheks_by_months[d[2]][d[1]] = 1

novichki, loyal, sleeping, predottok, ottok = 0, 0, 0, 0, 0  # инициализация счётчиков на каждый сегмент
cheks = 0  # инициализация счётчика чеков (для проверки совпадения с ихсодными данными)
clients_status = {}  # создаётся новый словарь для списка клиентов со статусами по сегментам

for client in clients:
    if len(clients[client]) == 1 and date_change(clients[client][0]) in (1, 2, 3):  # если длина списка дат клиента = 1
        # и давность покупки в пределах 3х месяцев, то это новичёк.
        novichki += 1  # +1 к счётчику новичков
        clients_status[client] = 'Новички'  # клиент попадает в новый список статусов клиентов со статусом новички
        cheks += len(clients[client])
        continue
    if len(clients[client]) > 1 and min(map(date_change, clients[client])) in (1, 2, 3):  # если длина списка дат
        # клиента > 1 и давность покупки в пределах 3х месяцев, то это лояльный
        loyal += 1  # +1 к счётчику лояльных
        clients_status[client] = 'Лояльные'  # клиент попадает в новый список статусов клиентов со статусом лояльные
        cheks += len(clients[client])
        continue
    if min(map(date_change, clients[client])) in (4, 5, 6):  # если давность покупки с 4го по 6й месяц, то это спящий.
        sleeping += 1  # +1 к счётчику спящих
        clients_status[client] = 'Спящие'  # клиент попадает в новый список статусов клиентов со статусом спящие
        cheks += len(clients[client])
        continue
    if min(map(date_change, clients[client])) in (7, 8, 9, 10, 11, 12):  # если давность покупки с 7го по 12й месяц,
        # то это предотток.
        predottok += 1  # +1 к счётчику предоттока
        clients_status[client] = 'Предотток'  # клиент попадает в новый список статусов клиентов со статусом предотток
        cheks += len(clients[client])
        continue
    if min(map(date_change, clients[client])) > 12:  # если давность покупки больше 12 месяцев, то это отток.
        ottok += 1  # +1 к счётчику оттока
        clients_status[client] = 'Отток'  # клиент попадает в новый список статусов клиентов со статусом отток
        cheks += len(clients[client])
        continue

# запишем данные по секторам у клиентов в csv-файл:
with open('clients_status1.csv', 'w', newline='', encoding="utf-8") as csvfile:
    clients_writer = csv.writer(csvfile, delimiter=';')
    clients_writer.writerow(['Guid', 'Сегмент'])
    for items in clients_status.items():
        clients_writer.writerow(items)

# запишем данные количества чеков по месяцам-годам:
with open('cheks_by_months1.csv', 'w', newline='', encoding="utf-8") as csvfile2:
    cheks_writer = csv.writer(csvfile2, delimiter=';')
    cheks_writer.writerow(('Месяц', '1', '2', '3', '4', '5', '6', '7',
                           '8', '9', '10', '11', '12', 'Итого:'))
    for items in cheks_by_months.items():
        lst = [val for val in items[1].values()]
        cheks_writer.writerow([items[0]] + lst + [sum(lst)])


print(f'________Итоги и проверочные суммы________',
      f'Новички: {novichki}',
      f'Лояльные: {loyal}',
      f'Спящие: {sleeping}',
      f'Предотток: {predottok}',
      f'Отток: {ottok}',
      f'Итого суммарно клиентов: {sum((novichki, loyal, sleeping, predottok, ottok))}',
      f'Всего чеков у клиентов (проверочная сумма для сравнения с файлом): {cheks}', sep='\n')

# for key1, dict in cheks_by_months.items():
#     print(f'_________{key1} год:_________')
#     [print(f'{key}-й месяц: {val}') for key, val in dict.items()]
