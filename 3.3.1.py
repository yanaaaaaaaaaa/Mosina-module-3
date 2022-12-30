import csv
import decimal
import requests
import xml.etree.ElementTree as ET

def my_split(s, seps, delete_empty=False, func=lambda x: x):
    ans = []
    t = ''
    for c in s:
        if c in seps:
            if (delete_empty and t != '') or not delete_empty:
                ans.append(func(t))
            t = ''
        else:
            t += c
    ans.append(func(t))
    return ans

def get_freq_and_minmax_date(filename, lower_limit=5000):
    freq_dict = dict()
    min_date = 2023, 12, 31, 23, 59, 59
    max_date = 2000, 12, 31, 23, 59, 59
    with open(filename, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        head = next(reader)
        for row in reader:
            if row[3] not in freq_dict:
                freq_dict[row[3]] = 0
            freq_dict[row[3]] += 1
            date = tuple(my_split(row[5], '-T:+', True, int)[:-1])
            if date < min_date:
                min_date = date
            if date > max_date:
                max_date = date

    #return freq_dict, min_date, max_date
    return list(filter(lambda x: freq_dict[x] > lower_limit, freq_dict)), min_date, max_date


def write_values_from_bank(min_date, max_date):
    for year in range(min_date[0], max_date[0] + 1):
        for month in range(1, 13):
            if year == max_date[0] and month > max_date[1]:
                 break
            if year == min_date[0] and month < min_date[1]:
                continue
            response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month:02}/{year}')
            with open(f'from_bank/01-{month}-{year}.xml','w') as response_file:
                response_file.write(response.text)


def compile_values_from_bank(currencies, min_date, max_date):
    with open('compile.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date'] + currencies)
        for year in range(min_date[0], max_date[0] + 1):
            for month in range(1, 13):
                if year == max_date[0] and month > max_date[1]:
                    break
                if year == min_date[0] and month < min_date[1]:
                    continue
                tree = ET.parse(f'from_bank/01-{month}-{year}.xml')
                row = [f'{year}-{month:02}']
                for curr in currencies:
                    value = tree.find(f"Valute[CharCode='{curr}']/Value")
                    if value != None:
                        row.append(decimal.Decimal(value.text.replace(',', '.')) / int(
                            tree.find(f"Valute[CharCode='{curr}']/Nominal").text))
                    else:
                        row.append('')
                writer.writerow(row)


#currencies, min_date, max_date = get_freq_and_minmax_date('vacancies_dif_currencies.csv')
#currencies = ['USD', 'EUR', 'KZT', 'UAH', 'BYR']
#min_date = 2005, 9, 16, 17, 26, 39
#max_date = 2022, 7, 18, 19, 35, 13
currencies = ['USD', 'EUR', 'KZT', 'UAH', 'BYR']
min_date = 2003, 1, 24, 21, 30, 49
max_date = 2022, 7, 19, 11, 10, 32


write_values_from_bank(min_date, max_date)
compile_values_from_bank(currencies, min_date, max_date)
