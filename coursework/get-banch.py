import csv

def binary_search_iterative(array, element, key):
    mid = 0
    start = 0
    end = len(array)
    step = 0

    while (start <= end):
        step = step+1
        mid = (start + end) // 2

        if element == array[mid][key]:
            return mid

        if element < array[mid][key]:
            end = mid - 1
        else:
            start = mid + 1
    return -1

def get_by_date(date="2017-08-08", name="PCLN", filename='dump.csv'):
    try:
        with open(filename, encoding='utf-8') as open_file:
            read_open_file = csv.DictReader(open_file)
            lst = []
            lst_final = []
            if date == name == 'all':
                return 'Выбраны все элементы файла'

            if date and name != 'all':
                for l in read_open_file:
                    if l['date'] == date and l['Name'] == name:
                        return list(l.values())

            for cache in read_open_file:
                lst.append(cache)
            if name == 'all':
                midle_element = binary_search_iterative(lst, date, 'date')
            for i in lst[midle_element:]:
                if i['date'] == date:
                    lst_final.append(list(i.values()))
                else:
                    break
            for i in lst[:midle_element + 1]:
                if i['date'] == date:
                    lst_final.append(list(i.values()))
                else:
                    return lst_final
            if date == 'all':
                midle_element = binary_search_iterative(lst, name, 'Name')
                for i in lst[midle_element:]:
                    if i['Name'] == date:
                        lst_final.append(list(i.values()))
                    else:
                        break
                for i in lst[:midle_element + 1]:
                    if i['Name'] == date:
                        lst_final.append(list(i.values()))
                    else:
                        return lst_final

    except FileNotFoundError:
        return 'File not found'

def start_get_by_date():
    print('Дата в формате yyyy-mm-dd [all]: ', end='')
    inp = input()
    date = inp
    if inp == '':
        date = 'all'

    print('Тикер [all]: ', end='')
    inp = input()
    name = inp
    if inp == '':
        name = 'all'

    print('Файл [filename]: ', end='')
    inp = input()
    filename = inp
    if inp == '':
        filename = 'dump.csv'

    print(get_by_date(date, name, filename))


if __name__ == '__main__':
    start_get_by_date()
