import csv
import os

def select_sorted(sort_columns=["high"], limit=30, group_by_name=False, order='desc', filename='dump.csv'):
    list_file = []
    def partition(items, low, high, sort_columns):
        '''
        расчет индекса и замена элементов при сортировке quick_sort
        '''
        # Выбираем средний элемент в качестве опорного
        # Также возможен выбор первого, последнего
        # или произвольного элементов в качестве опорного
        pivot = items[(low + high) // 2][sort_columns[0]]
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while float(items[i][sort_columns[0]]) < float(pivot):
                i += 1
            j -= 1
            while float(items[j][sort_columns[0]]) > float(pivot):
                j -= 1
            if i >= j:
                return j
            # Если элемент с индексом i (слева от опорного) больше, чем
            # элемент с индексом j (справа от опорного), меняем их местами
            items[i], items[j] = items[j], items[i]


    def quick_sort(items, sort_columns):
        '''
        реализация функции сортировки quick_sort
        '''
        # Создадим вспомогательную функцию, которая вызывается рекурсивно

        def _quick_sort(items, low, high, sort_columns):
            if low < high:
                # This is the index after the pivot, where our lists are split
                split_index = partition(items, low, high, sort_columns)
                _quick_sort(items, low, split_index, sort_columns)
                _quick_sort(items, split_index + 1, high, sort_columns)
        return _quick_sort(items, 0, len(items) - 1, sort_columns)


    try:
        with open(filename, 'r', encoding='utf-8', newline='') as open_cache_file:
            reader_cache_file = csv.DictReader(open_cache_file)
            for cache in reader_cache_file:
                if cache['request'] == str([sort_columns, limit, group_by_name, order, filename]):
                    return cache['answer']
        raise Exception
    except:
        if group_by_name:
            with open('all_stocks_5yr.csv', encoding='utf-8', newline='') as open_file:
                filename_reader = csv.DictReader(open_file)

                for line in filename_reader:
                    if line[sort_columns[0]] == '':
                        line[sort_columns[0]] = '0'
                    list_file.append(line)


                '''
                Если присутствует фильтрация по нейму, то фильтруем весь файл по нейму и создаем файлы содержащие один нейм, 
                после чего проходимся по каждому файлу, фильтруем его по выбранному параметру и соединяем файлы
                '''
                list_name_middle_file = []
                list_for_middle_file = []
                for l in range(len(list_file)):
                    if list_for_middle_file == []:
                        list_for_middle_file.append(list_file[l])
                        continue
                    if l == len(list_file) -1 and list_file[l]["Name"] == list_file[l-1]["Name"]:
                        list_for_middle_file.append(list_file[l])
                        break
                    if list_file[l]["Name"] == list_file[l+1]["Name"]:
                        list_for_middle_file.append(list_file[l])
                        continue
                    else:
                        list_for_middle_file.append(list_file[l])
                        name_middle_file = list_file[l]["Name"] + '.csv'
                        if list_file[l]["Name"] == '':
                            name_middle_file = '1_.csv'
                        list_name_middle_file.append(name_middle_file)
                        with open(name_middle_file, 'w', encoding='utf-8', newline='') as middle_file:
                            fieldnames_middle_file = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                            write_middle_file = csv.DictWriter(middle_file, fieldnames=fieldnames_middle_file)
                            write_middle_file.writeheader()
                            for name_line in list_for_middle_file:
                                write_middle_file.writerow(name_line)
                            list_for_middle_file = []
                list_file = []
                if order == 'desc':
                    final_list = []
                    ind = -1
                    while True:
                        name = list_name_middle_file[ind]
                        with open(name, 'r', encoding='utf-8') as middle_file_r:
                            read_middle_file_r = csv.DictReader(middle_file_r)
                            for line_ in read_middle_file_r:
                                list_file.append(line_)
                            quick_sort(list_file, sort_columns)
                            list_file = list_file[::-1]
                            final_list += list_file
                            list_file = []
                            if len(final_list) < limit:    #если длинна конечного списка меньше лимита, открываем следующий файл и
                                ind -= 1
                            else:   #если длинна больше или равна лимиту, то выходим из цикла
                                break
                    with open(filename, 'a', encoding='utf-8', newline="") as cache_file:
                        fieldnames = ['request', 'answer']
                        write_cache_file = csv.DictWriter(cache_file, fieldnames=fieldnames)
                        size = os.path.getsize('dump.csv')
                        if size == 0:
                            write_cache_file.writeheader()
                        answer = []
                        for i in range(limit):
                            answer.append(list(final_list[i].values()))
                        write_cache_file.writerow({'request': [sort_columns, limit, group_by_name, order, filename], 'answer': answer})
                        return answer
                else:
                    final_list = []
                    ind = 0
                    while True:
                        name = list_name_middle_file[ind]
                        with open(name, 'r', encoding='utf-8') as middle_file_r:
                            read_middle_file_r = csv.DictReader(middle_file_r)
                            for line_ in read_middle_file_r:
                                list_file.append(line_)
                            quick_sort(list_file, sort_columns)
                            final_list += list_file
                            list_file = []
                            if len(final_list) < limit:  # если длинна конечного списка меньше лимита, открываем следующий файл и
                                ind += 1
                            else:  # если длинна больше или равна лимиту, то выходим из цикла
                                break
                    with open(filename, 'a', encoding='utf-8', newline="") as cache_file:
                        fieldnames = ['request', 'answer']
                        write_cache_file = csv.DictWriter(cache_file, fieldnames=fieldnames)
                        size = os.path.getsize('dump.csv')
                        if size == 0:
                            write_cache_file.writeheader()
                        answer = []
                        for i in range(limit):
                            answer.append(list(final_list[i].values()))
                        write_cache_file.writerow(
                            {'request': [sort_columns, limit, group_by_name, order, filename], 'answer': answer})
                        return answer
        '''
        сортировка без нейма
        '''
        if order == 'asc':
            with open('all_stocks_5yr.csv', encoding='utf-8', newline='') as open_file:
                filename_reader = csv.DictReader(open_file)
                count = 0
                count_file = 0
                list_file = []
                list_name_file = []

                for line in filename_reader:
                    if line[sort_columns[0]] == '':
                        line[sort_columns[0]] = '0'
                    list_file.append(line)
                    count +=1

                    if count == 200000:
                        count_file += 1
                        quick_sort(list_file, sort_columns)
                        name = str(count_file) + 'file.csv'
                        list_name_file.append(name)
                        with open(name, 'w', encoding='utf-8', newline='') as new_file:
                            fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                            write_new_file = csv.DictWriter(new_file, fieldnames=fieldnames)
                            write_new_file.writeheader()
                            for st in list_file:
                                write_new_file.writerow(st)
                            count = 0
                            list_file = []

                if list_file != []: # если после завершения цикла в списке остались эл-ты, то дополнительно заводим файл
                    count_file += 1
                    quick_sort(list_file, sort_columns)
                    name = str(count_file) + 'file.csv'
                    list_name_file.append(name)
                    with open(name, 'w', encoding='utf-8', newline='') as new_file:
                        fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                        write_new_file = csv.DictWriter(new_file, fieldnames=fieldnames)
                        write_new_file.writeheader()

                        for st in list_file:
                            write_new_file.writerow(st)

                for i in range(len(list_name_file)):

                    file_i = open(list_name_file[i])
                    reader_i = csv.DictReader(file_i)
                    name_result = str(i + 1) + 'result.csv'
                    result_file = open(name_result, 'w')
                    fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                    result_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
                    result_writer.writeheader()

                    if i == 0:
                        for w in reader_i:
                            result_writer.writerow(w)
                    else:
                        name_second = str(i) + 'result.csv'
                        file_second = open(name_second)
                        reader_file_second = csv.DictReader(file_second)

                        next_file_i = reader_i.__next__()
                        next_file_second = reader_file_second.__next__()

                        while True:
                            if float(next_file_i[sort_columns[0]]) > float(next_file_second[sort_columns[0]]):
                                result_writer.writerow(next_file_second)
                                try:
                                    next_file_second = reader_file_second.__next__()
                                except:
                                    for w in reader_i:
                                        result_writer.writerow(w)
                                    break

                            else:
                                result_writer.writerow(next_file_i)
                                try:
                                    next_file_i = reader_i.__next__()
                                except:
                                    for w in reader_file_second:
                                        result_writer.writerow(w)
                                    break
                        file_second.close()
                    file_i.close()
                    result_file.close()
                answer = []
                with open(str(len(list_name_file))+'result.csv', 'r', encoding='utf-8', newline="") as result_file:
                    read_result_file = csv.DictReader(result_file)
                    count = 0
                    for i in read_result_file:
                        if count == limit:
                            break
                        answer.append(list(i.values()))
                        count += 1

                with open(filename, 'a', encoding='utf-8', newline="") as cache_file:
                    fieldnames = ['request', 'answer']
                    write_cache_file = csv.DictWriter(cache_file, fieldnames=fieldnames)
                    size = os.path.getsize('dump.csv')
                    if size == 0:
                        write_cache_file.writeheader()
                    write_cache_file.writerow({'request': [sort_columns, limit, group_by_name, order, filename], 'answer': answer})
                    return answer
        '''
        обратная сортировка
        '''
        if order == 'desc':
            with open('all_stocks_5yr.csv', encoding='utf-8', newline='') as open_file:
                filename_reader = csv.DictReader(open_file)
                count = 0
                count_file = 0
                list_file = []
                list_name_file = []

                for line in filename_reader:
                    if line[sort_columns[0]] == '':
                        line[sort_columns[0]] = '0'
                    list_file.append(line)
                    count += 1

                    if count == 200000:
                        count_file += 1
                        quick_sort(list_file, sort_columns)
                        list_file = list_file[::-1]
                        name = str(count_file) + 'file.csv'
                        list_name_file.append(name)
                        with open(name, 'w', encoding='utf-8', newline='') as new_file:
                            fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                            write_new_file = csv.DictWriter(new_file, fieldnames=fieldnames)
                            write_new_file.writeheader()
                            for st in list_file:
                                write_new_file.writerow(st)
                            count = 0
                            list_file = []

                if list_file != []:  # если после завершения цикла в списке остались эл-ты, то дополнительно заводим файл
                    count_file += 1
                    quick_sort(list_file, sort_columns)
                    list_file = list_file[::-1]
                    name = str(count_file) + 'file.csv'
                    list_name_file.append(name)
                    with open(name, 'w', encoding='utf-8', newline='') as new_file:
                        fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                        write_new_file = csv.DictWriter(new_file, fieldnames=fieldnames)
                        write_new_file.writeheader()

                        for st in list_file:
                            write_new_file.writerow(st)

                for i in range(len(list_name_file)):

                    file_i = open(list_name_file[i])
                    reader_i = csv.DictReader(file_i)
                    name_result = str(i + 1) + 'result.csv'
                    result_file = open(name_result, 'w')
                    fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'Name']
                    result_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
                    result_writer.writeheader()

                    if i == 0:
                        for w in reader_i:
                            result_writer.writerow(w)
                    else:
                        name_second = str(i) + 'result.csv'
                        file_second = open(name_second)
                        reader_file_second = csv.DictReader(file_second)

                        next_file_i = reader_i.__next__()
                        next_file_second = reader_file_second.__next__()

                        while True:
                            if float(next_file_i[sort_columns[0]]) < float(next_file_second[sort_columns[0]]):
                                result_writer.writerow(next_file_second)
                                try:
                                    next_file_second = reader_file_second.__next__()
                                except:
                                    for w in reader_i:
                                        result_file.writerow(w)
                                    break

                            else:
                                result_writer.writerow(next_file_i)
                                try:
                                    next_file_i = reader_i.__next__()
                                except:
                                    for w in reader_file_second:
                                        result_writer.writerow(w)
                                    break
                        file_second.close()
                    file_i.close()
                    result_file.close()
                answer = []
                with open(str(len(list_name_file)) + 'result.csv', 'r', encoding='utf-8', newline="") as result_file:
                    read_result_file = csv.DictReader(result_file)
                    count = 0
                    for i in read_result_file:
                        if count == limit:
                            break
                        answer.append(list(i.values()))
                        count += 1

                with open(filename, 'a', encoding='utf-8', newline="") as cache_file:
                    fieldnames = ['request', 'answer']
                    write_cache_file = csv.DictWriter(cache_file, fieldnames=fieldnames)
                    size = os.path.getsize('dump.csv')
                    if size == 0:
                        write_cache_file.writeheader()
                    write_cache_file.writerow(
                        {'request': [sort_columns, limit, group_by_name, order, filename], 'answer': answer})
                    return answer



def start_select_sorted():
    print('Сортировать по цене\nоткрытия (1)\nзакрытия (2)\nмаксимум [3]\nминимум (4)\nобъем (5)')
    inp = input()
    if inp == '' or '3':
        sort_columns = ['high']
    if inp == '1':
        sort_columns = ['open']
    if inp == '2':
        sort_columns = ['close']
    if inp == '4':
        sort_columns = ['low']
    if inp == '5':
        sort_columns = ['volume']

    print('Порядок по убыванию [1] / возрастанию (2): ', end='')
    inp = input()
    if inp == '' or '1':
        order='desc'
    if inp == '2':
        order = 'asc'

    print('Ограничение выборки [10]: ', end='')
    inp = input()
    limit = 10
    if inp.isdigit():
        limit = int(inp)

    print('Название файла для сохранения результата [dump.csv]: ', end='')
    inp = input()
    filename = inp
    if inp == '':
        filename = 'dump.csv'

    print(select_sorted(sort_columns= sort_columns, limit= limit, order= order, filename= filename))




if __name__ == '__main__':
    start_select_sorted()



