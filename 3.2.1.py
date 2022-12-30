import csv

class Vacancy:
    def __init__(self, **kwargs):
        self.salary_currency = kwargs['salary_currency']
        self.area_name = kwargs['area_name']
        self.name = kwargs['name']
        self.__set_published_at(kwargs['published_at'])
        self.salary = (float(kwargs['salary_from']) + float(kwargs['salary_to'])) // 2

    def __set_published_at(self, published_at):
        spliten = published_at.split('T')
        date = spliten[0].split('-')
        self.year = int(date[0])


class DataSet:
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
        "UZS": 0.0055}

    def __init__(self, header):
        self.header = header
        self.vacancies: list[Vacancy] = []

    def print_stats(self, vacancy_name, stats=None):
        if stats is None:
            stats = self.get_stats(vacancy_name)

        print('Динамика уровня зарплат по годам:', stats['salary_stat'])
        print('Динамика количества вакансий по годам:', stats['vacancy_count_stat'])
        print('Динамика уровня зарплат по годам для выбранной профессии:', stats['selected_salary_stat'])
        print('Динамика количества вакансий по годам для выбранной профессии:', stats['selected_count_stat'])
        print('Уровень зарплат по городам (в порядке убывания):',
              {k: stats['area_salary_stat'][k] for i, k in zip(range(10), stats['area_salary_stat'])})
        print('Доля вакансий по городам (в порядке убывания):', {k: stats['doly_stat'][k] for i, k in zip(range(10), stats['doly_stat'])})

    def get_stats(self, vacancy_name):
        vacancies = self.vacancies
        doly_stat = dict()
        salary_stat = dict()
        vacancy_count_stat = dict()
        selected_salary_stat = dict()
        selected_count_stat = dict()
        area_salary_stat = dict()
        area_count_stat = dict()
        for vacancy in vacancies:
            salary = int(vacancy.salary * DataSet.currency_to_rub[vacancy.salary_currency])
            if vacancy.area_name not in doly_stat:
                doly_stat[vacancy.area_name] = 0
                area_salary_stat[vacancy.area_name] = 0
                area_count_stat[vacancy.area_name] = 0
            doly_stat[vacancy.area_name] += 1
            area_salary_stat[vacancy.area_name] += salary
            area_count_stat[vacancy.area_name] += 1

            if vacancy.year not in salary_stat:
                salary_stat[vacancy.year] = 0
                vacancy_count_stat[vacancy.year] = 0
                selected_salary_stat[vacancy.year] = 0
                selected_count_stat[vacancy.year] = 0
            salary_stat[vacancy.year] += salary
            vacancy_count_stat[vacancy.year] += 1
            if vacancy_name in vacancy.name:
                selected_salary_stat[vacancy.year] += salary
                selected_count_stat[vacancy.year] += 1

        doly_stat = {k: doly_stat[k] / len(vacancies) for k in doly_stat if doly_stat[k] >= int(len(vacancies) / 100)}
        doly_stat = {k: round(doly_stat[k], 4) for k in sorted(doly_stat, key=lambda k: -doly_stat[k])}
        salary_stat = {k: salary_stat[k] // vacancy_count_stat[k] for k in sorted(salary_stat)}
        selected_salary_stat = {k: selected_salary_stat[k] // selected_count_stat[k] if selected_count_stat[k] != 0 else 0 for k in sorted(selected_salary_stat)}
        area_salary_stat = {k: area_salary_stat[k] // area_count_stat[k] for k in area_salary_stat if k in doly_stat}
        area_salary_stat = {k: area_salary_stat[k] for k in sorted(area_salary_stat, key=lambda k: -area_salary_stat[k])}
        return {'doly_stat': doly_stat, 'vacancy_count_stat': vacancy_count_stat, 'salary_stat': salary_stat, 'area_salary_stat': area_salary_stat, 'selected_salary_stat': selected_salary_stat, 'selected_count_stat': selected_count_stat}

def read_csv(filename):
    with open(filename, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        header = next(reader)
        data_set = DataSet(header)
        data_set.vacancies = [Vacancy(**{k: v for k, v in zip(header, line)}) for line in reader if len(line) == len(header) and all(line)]
    return data_set


def separate_by_year(file_name):
    files = {}
    writers = {}
    path = r'files/'
    with open(file_name, encoding='utf-8-sig') as globfile:
        reader = csv.reader(globfile)
        header = next(reader)
        for row in reader:
            if len(row) != len(header) or not all(row):
                continue
            year = row[5].split('-')[0]
            if year not in files:
                files[year] = open(f'{path}{year}_chank.csv', 'w', newline='', encoding='utf-8-sig')
                writers[year] = csv.writer(files[year])
                writers[year].writerow(header)
            writers[year].writerow(row)
    for year in files:
        files[year].close()

file_name = input('Введите название файла: ')
separate_by_year(file_name)