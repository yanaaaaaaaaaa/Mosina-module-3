import requests, json, time
import csv

base_url = 'https://api.hh.ru'

def get_vacancies(params):
    global base_url
    req = requests.get(f'{base_url}/vacancies', params)
    if req.status_code != 200:
        for i in range(100):
            time.sleep(0.3)
            req = requests.get(f'{base_url}/vacancies', params)
            if req.status_code == 200:
                break
            else:
                if 'captha' in req.content.decode():
                    print(req.content.decode())
                    input()
                    time.sleep(5)
    data = req.content.decode()
    req.close()
    return data

params = {
        'page': 0,
        'per_page': 100,
        'specialization': 1,
        'date_from': '2022-12-19T00:00:00+0300',
        'date_to':  '2022-12-19T06:00:00+0300'
    }

dates_from = ['2022-12-19T00:00:00+0300', '2022-12-19T06:00:00+0300', '2022-12-19T12:00:00+0300', '2022-12-19T18:00:00+0300']
dates_to = ['2022-12-19T06:00:00+0300', '2022-12-19T12:00:00+0300', '2022-12-19T18:00:00+0300', '2022-12-19T23:59:59+0300']


with open('19-12-2022.csv', 'w',encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    head = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']
    writer.writerow(head)

    for i in range(4):
        params['date_to'] = dates_to[i]
        params['date_from'] = dates_from[i]
        for page in range(20):
            params['page'] = page
            jsn = json.loads(get_vacancies(params))
            for d in jsn['items']:
                row = [d['name']]
                if d['salary'] != None:
                    row.extend([d['salary']['from'], d['salary']['to'], d['salary']['currency']])
                else:
                    row.extend([None, None, None])
                if d['area'] != None:
                    row.append(d['area']['name'])
                else:
                    row.append(None)
                row.append(d['published_at'])
                writer.writerow(row)
            time.sleep(0.25)
        if i != 3:
            time.sleep(5)


