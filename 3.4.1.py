import pandas as pd
import csv

compile = dict()

with open('compile.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    compile_head = next(reader)
    for line in reader:
        compile[tuple(line[0].split('-'))] = {k: v for k, v in zip(compile_head, line)}


def get_salary(s_from, s_to, s_currency, published_at):
    year, month = published_at.split('T')[0].split('-')[:2]
    if (s_to == 0 and s_from == 0) or (year, month) not in compile or s_currency == '':
        return None
    d = compile[year, month]
    if s_currency not in d or d[s_currency] == '':
        return None
    salary = 0
    count = 0
    if s_from != 0:
        salary += s_from
        count += 1
    if s_to != 0:
        salary += s_to
        count += 1
    if s_currency != 'RUR':
        salary *= float(d[s_currency])
    return salary // count

df = pd.read_csv('vacancies_dif_currencies.csv', encoding='utf-8-sig').fillna(0)
df['salary'] = df.apply(lambda row: get_salary(row['salary_from'], row['salary_to'], row['salary_currency'], row['published_at']), axis=1)
print('****')
with open('file_with_pandas.csv', 'w', encoding='utf-8-sig', newline='') as file:
    df[['name', 'salary', 'area_name', 'published_at']][:100].to_csv(file, index=False)


