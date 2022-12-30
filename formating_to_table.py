import re
import prettytable as prt
import functools

eng_to_ru = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки', 'experience_id':
    'Опыт работы', 'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата и время публикации вакансии'
}

exp_dict = {
    "Более 6 лет": 3,
    "От 3 до 6 лет": 2,
    "От 1 года до 3 лет": 1,
    "Нет опыта": 0
}


currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}
ru_to_eng = {eng_to_ru[key]: key for key in eng_to_ru}

money_ru = {eng_to_ru[key]: val for key, val in currency_to_rub.items()}
ru_to_eng['Оклад'] = ''
ru_to_eng['Дата публикации вакансии'] = ''



class DataSet:

    def __init__(self, filename):
        self.file_name = filename
        self.vacancies_objects = []

    def filter(self, field, param):
        pass

    def sort(self, field, param):
        pass


    def print_as_table(self, input_con):
        fields = ['№'] + list(self.vacancies_objects[0].field_dict.keys())
        table = prt.PrettyTable()
        table.field_names = fields
        self.fil_table(table)
        start = input_con.start
        end = input_con.end if input_con.end is not None else len(self.vacancies_objects)
        print(table.get_string(start=start, end=end, fields=input_con.fields))

    def fil_table(self, table):
        i = 1
        for vacancy in self.vacancies_objects:
            vacancy.fil_dict()
            row = [i]
            for field in vacancy.field_dict:
                row.append(vacancy.field_dict[field])
            table.add_row(row)
            i += 1

class Salary:
    def __init__(self):
        self.salary_from = None
        self.salary_to = None
        self.salary_gross = None
        self.salary_currency = None

    def get_gross_as_str_ru(self):
        if self.salary_gross.lower() == 'true':
            return 'Без вычета налогов'
        return 'С вычетом налогов'

    def get_as_str_ru(self):
        return f'{self.salary_from} - {self.salary_to} ({Vacancy.eng_to_ru[self.salary_currency]}) ({self.get_gross_as_str_ru()}) '


class Vacancy:

    def __init__(self):
        self.field_dict = None
        self.name = None
        self.description = None
        self.key_skills = None
        self.experience_id = None
        self.premium = None
        self.employer_name = None
        self.salary = None
        self.area_name = None
        self.published_at = None

    def format_date(self):
        pass

    def fil_dict(self):
        self.field_dict = {
            'Название': self.name,
            'Описанеи': self.description,
            'Навыки': self.key_skills,
            'Опыт работы': Vacancy.eng_to_ru[self.experience_id],
            'Премиум-вакансия': 'Да',
            'Компания': self.employer_name,
            'Оклад': self.salary.get_as_str_ru(),
            'Название региона': self.area_name,
            'Дата публикации вакансии': self.published_at
        }
        if self.premium.lower() == 'false':
            self.field_dict['Премиум-вакансия'] = 'Нет'

def csv_reader(file_name):
    import csv
    with open(file_name, encoding='utf-8-sig') as f:
        data = [row for row in csv.reader(f)]
    if len(data) == 0:
        print('Пустой файл')
        exit()
    elif len(data) == 1:
        print('Нет данных')
        exit()
    list_naming = data.pop(0)
    all_vacan = list(filter(lambda row: len(row) == len(list_naming) and all(row), data))
    return all_vacan, list_naming

def format_str(s):
    lower_s = s.lower()
    if lower_s == 'false':
        return 'Нет'
    elif lower_s == 'true':
        return 'Да'
    return ' '.join(re.sub(r'<[^<>]*>', '', s).split())


def do_format(cell):
    return list(map(format_str, cell.split('\n')))


def csv_filter(all_vacan, list_naming):
    return [{name: do_format(cell) for cell, name in zip(vacan, list_naming)} for vacan in all_vacan ]


def do_ru_vacancies(data_vacancies, dic_naming):
    return [{dic_naming[key]: dictionary[key] for key in dictionary} for dictionary in data_vacancies]


def format_time(s):
    return ['.'.join(reversed(s.split('T')[0].split('-')))]


def format_nalog(d):
    if d['Оклад указан до вычета налогов'][0] == 'Да':
        return 'Без вычета налогов'
    return 'С вычетом налогов'


def format_numbers(s):
    s = s.split('.')[0]
    x = int(s)
    return '{0:,}'.format(x).replace(',', ' ')


def format_oklad(d):
    return [f'{format_numbers(d["Нижняя граница вилки оклада"][0])} - {format_numbers(d["Верхняя граница вилки оклада"][0])} ({eng_to_ru[d["Идентификатор валюты оклада"][0]]}) ({format_nalog(d)})']


def formatter(d):
    new_d = {}
    for key in d:
        if key == 'Нижняя граница вилки оклада':
            break
        if key == 'Опыт работы':
            new_d[key] = [eng_to_ru[d[key][0]]]
        else:
            new_d[key] = d[key]
    new_d['Оклад'] = format_oklad(d)
    new_d['Название региона'] = d['Название региона']
    new_d['Дата публикации вакансии'] = format_time(d['Дата и время публикации вакансии'][0])
    #new_d['Дата публикации вакансии'] = d['Дата и время публикации вакансии']
    return new_d


def for_all_form(ru_name_vacan):
    new_ = []
    for d in ru_name_vacan:
        new_.append(formatter(d))
    return new_


def print_vacancies(ru_name_vacan):
    for d in ru_name_vacan:
        new_d = formatter(d)
        for name_ru in new_d:
            print(f'{name_ru}:', ', '.join(new_d[name_ru]))
        print()


def fill_table(table, data):
    i = 1
    table.field_names = ['№'] + list(ru_name_vacan[0].keys())
    for d in data:
        row = [i]
        for key in d:
            cell = functools.reduce(lambda x, y: x + '\n' + y, d[key])
            if len(cell) > 100:
                row.append(cell[:100] + '...')
            else:
                row.append(cell)
        table.add_row(row)
        i += 1
    return table


def format_table(table):
    table.hrules = prt.ALL
    table.max_width = 20
    table.align = 'l'


def check_filter(s):
    if s == '':
        return
    if ':' not in s:
        print("Формат ввода некорректен")
        exit()
    spliten = s.split(': ')
    if spliten[0] not in ru_to_eng:
        print("Параметр поиска некорректен")
        exit()


def parse_oklad(s):
    spliten = s.split(' (')[0].split(' - ')
    bottom = int(''.join(spliten[0].split()))
    top = int(''.join(spliten[1].split()))
    return (top + bottom) / 2

def parse_id(s):
    return s.split(' (')[1].split(')')[0]



def filter_oklad(ru_name_vacan, filter):
    new_l = []
    for d in ru_name_vacan:
        spliten = d['Оклад'][0].split(' (')[0].split(' - ')
        bottom = int(''.join(spliten[0].split()))
        top = int(''.join(spliten[1].split()))
        if bottom<= filter <= top:
            new_l.append(d)
    return new_l


def filter_date(ru_name_vacan, filter):
    new_l = []
    for d in ru_name_vacan:
        day,m,y =  d['Дата публикации вакансии'][0].split('.')
        if filter[0] == day and filter[1] == m and filter[2] == y:
            new_l.append(d)
    return new_l


def filter_other(ru_name_vacan, filter_val, filter_key):
    new_l = []
    for d in ru_name_vacan:
        if all(val in d[filter_key] for val in filter_val):
            new_l.append(d)
    return new_l


def filter_idval(ru_name_vacan, filter):
    new_l = []
    for d in ru_name_vacan:
        spliten = d['Оклад'][0].split(' (')[1].split(')')
        if filter == spliten[0]:
            new_l.append(d)
    return new_l


def filter_vacan(ru_name_vacan, filter):
    if filter == '':
        return ru_name_vacan
    spliten = filter.split(': ')
    if spliten[0] == 'Оклад':
        return filter_oklad(ru_name_vacan, int(spliten[1]))
    elif spliten[0] == 'Дата публикации вакансии':
        return filter_date(ru_name_vacan, spliten[1].split('.'))
    elif spliten[0] == 'Идентификатор валюты оклада':
        return filter_idval(ru_name_vacan, spliten[1])
    return filter_other(ru_name_vacan, spliten[1].split(', '), spliten[0])


def check_sort(s):
    if s != '' and s not in ru_to_eng:
        print('Параметр сортировки некорректен')
        exit()



def sort_oklad(vacan, reverse):
    return sorted(vacan, key=lambda d: parse_oklad(d['Оклад'][0]) * money_ru[parse_id(d['Оклад'][0])], reverse=reverse)


def sort_exp(vacan, reverse):
    return sorted(vacan, key=lambda d: exp_dict[d['Опыт работы'][0]], reverse=reverse)


def sort_date(vacan, reverse):
    def parse_date(s):
        spliten = s.split('T')
        y, m, day = map(int, spliten[0].split('-'))
        hour, minute, sec = map(int, spliten[1].split('+')[0].split(':'))
        return y, m, day, hour, minute, sec

    return sorted(vacan, key=lambda d: parse_date(d['Дата и время публикации вакансии'][0]), reverse = reverse)


def sort_skills(vacan, reverse):
    vacan.sort(key=lambda d: len(d['Навыки']), reverse=reverse)
    return vacan


def sort_other(vacan, key_, reverse):
    return sorted(vacan, reverse=reverse,key=lambda d: d[key_][0])


def sort_vacan(vacan, sort_by, revers):
    if sort_by in ['', 'Дата публикации вакансии']:
        return vacan
    if sort_by == 'Оклад':
        return sort_oklad(vacan, revers)
    if sort_by == 'Навыки':
        return sort_skills(vacan, revers)
    if sort_by == 'Опыт работы':
        return sort_exp(vacan, revers)
    return sort_other(vacan, sort_by, revers)

class InputConnect:
    def start_connection(self):
        self.file_name = input("Введите название файла: ")
        self.filter_for_fields = input('Введите параметр фильтрации: ')
        self.sort_by = input("Введите параметр сортировки: ")
        self.revers_sort = input('Обратный порядок сортировки (Да / Нет): ')
        self.se = input('Введите диапазон вывода: ').split()
        self.inp = input('Введите требуемые столбцы: ').split(', ')
        if self.sort_by != '' and self.sort_by not in self.inp:
            self.inp.append(self.sort_by)
        check_filter(self.filter_for_fields)
        check_sort(self.sort_by)
        if self.revers_sort == 'Да' or self.revers_sort == 'Нет' or self.revers_sort == '':
            self.revers_sort = self.revers_sort == 'Да'
        else:
            print('Порядок сортировки задан некорректно')
            exit()


inp = InputConnect()
inp.start_connection()


all_vacan, list_naming = csv_reader(inp.file_name)
data_vacancies = csv_filter(all_vacan, list_naming)
ru_name_vacan_all = do_ru_vacancies(data_vacancies, eng_to_ru)
if inp.sort_by == 'Дата публикации вакансии':
    ru_name_vacan_all = sort_date(ru_name_vacan_all, inp.revers_sort)
ru_name_vacan = for_all_form(ru_name_vacan_all)
ru_name_vacan = filter_vacan(ru_name_vacan, inp.filter_for_fields)
if len(ru_name_vacan) == 0:
    print('Ничего не найдено')
    exit()
ru_name_vacan = sort_vacan(ru_name_vacan, inp.sort_by, inp.revers_sort)

table = prt.PrettyTable()
table = fill_table(table, ru_name_vacan)
format_table(table)
strt = 0
end = len(ru_name_vacan)
if len(inp.se) > 0:
    strt = int(inp.se[0]) - 1
if len(inp.se) == 2:
    end = int(inp.se[1]) - 1
fields = table.field_names
if '' not in inp.inp:
    fields = ['№'] + inp.inp
print(table.get_string(start=strt,end=end,fields=fields))


