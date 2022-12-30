import pandas as pd
import pdfkit
from jinja2 import Environment, FileSystemLoader


def get_stats(filename, vacancy_name):
    df = pd.read_csv(filename, encoding='utf-8-sig')\
            .dropna()\
            .assign(salary=lambda x: x['salary'].astype('int64'),
                    area_name=lambda x: x['area_name'].astype('category'))\
            .assign(year=lambda x: x.apply(lambda y: y['published_at'].split('T')[0].split('-')[0], axis=1))
    salary_stat = df[['year', 'salary']].groupby('year').mean().round().to_dict()['salary']
    selected_salary_stat = df[df.name.apply(lambda x: vacancy_name.lower() in x.lower())][['year', 'salary']].groupby('year').mean().round().to_dict()['salary']
    count_stat = df.groupby('year').count().to_dict()['salary']
    selected_count_stat = df[df.name.apply(lambda x: vacancy_name.lower() in x.lower())].groupby('year').count().to_dict()['salary']
    header = ['year',
              'salary by year',
              'salary by year for selected vacancy',
              'number of vacancies',
              'number of vacancies for selected vacancy']
    d = dict()
    for year in salary_stat:
        d[year] = dict()
        d[year][header[0]] = year
        d[year][header[1]] = salary_stat[year]
        d[year][header[2]] = selected_salary_stat[year]
        d[year][header[3]] = count_stat[year]
        d[year][header[4]] = selected_count_stat[year]

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("pdf_template.html")
    pdf_template = template.render({'header': header, 'd': d})
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(pdf_template, '3.4.2.pdf', configuration=config)

    print('Динамика уровня зарплат по годам:', salary_stat)
    print('Динамика уровня зарплат по годам для выбранной профессии:', selected_salary_stat)
    print('Динамика количества вакансий по годам:', count_stat)
    print('Динамика количества вакансий по годам для выбранной профессии:',selected_count_stat)


filename = input()
vacancy_name = input()

get_stats(filename, vacancy_name)
