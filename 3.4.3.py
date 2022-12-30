import pandas as pd
import pdfkit
from jinja2 import Environment, FileSystemLoader


def get_stats(filename, vacancy_name, area_name):
    df = pd.read_csv(filename, encoding='utf-8-sig')\
            .dropna()\
            .assign(area_name=lambda x: x['area_name'].astype('category'))\
            .assign(year=lambda x: x.apply(lambda y: y['published_at'].split('T')[0].split('-')[0], axis=1))
    len_df = len(df)
    one_proc = len_df // 100
    print(one_proc)
    salary_by_area = df.groupby('area_name')['salary'].agg(['count', 'mean']).query(f'count > {one_proc}')['mean'].sort_values(ascending=False).round(2).head(10).to_dict()
    fraction_by_area = df.groupby('area_name').count()['salary']
    fraction_by_area = fraction_by_area[fraction_by_area > one_proc] / len_df
    fraction_by_area = fraction_by_area.round(3).head(10).to_dict()

    selected_salary_stat = df[df.name.apply(lambda x: vacancy_name.lower() in x.lower())][df.area_name.apply(lambda x: area_name.lower() == x.lower())][['year', 'salary']].groupby('year').mean().round().to_dict()['salary']
    selected_count_stat = df[df.name.apply(lambda x: vacancy_name.lower() in x.lower())][df.area_name.apply(lambda x: area_name.lower() == x.lower())].groupby('year').count().to_dict()['salary']

    header_1 = ['year',
              'salary by year for selected vacancy and area',
              'number of vacancies for selected vacancy and area']

    header_2 = ['area', 'salary by area', 'fraction by area']
    d_area = dict()
    for area in salary_by_area:
        d_area[area] = dict()
        d_area[area][header_2[0]] = area
        d_area[area][header_2[1]] = salary_by_area[area]
        d_area[area][header_2[2]] = fraction_by_area[area]

    d_year = dict()
    for year in selected_salary_stat:
        d_year[year] = dict()
        d_year[year][header_1[0]] = year
        d_year[year][header_1[1]] = selected_salary_stat[year]
        d_year[year][header_1[2]] = selected_count_stat[year]

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("pdf_template_for_3.4.3.html")
    pdf_template = template.render({'header_1': header_1, 'd_area': d_area, 'd_year': d_year, 'header_2': header_2})
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(pdf_template, '3.4.3.pdf', configuration=config)

    print('Уровень зарплат по городам: ', salary_by_area)
    print('Доля вакансий по городам: ', fraction_by_area)
    print('Динамика уровня зарплат по годам для выбранной профессии:', selected_salary_stat)
    print('Динамика количества вакансий по годам для выбранной профессии:',selected_count_stat)

filename = input()
vacancy_name = input()
area_name = input()

get_stats(filename, vacancy_name, area_name)
