import csv

filename = 'vacancies_dif_currencies.csv'
compile = dict()

with open('compile.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    compile_head = next(reader)
    for line in reader:
        compile[tuple(line[0].split('-'))] = {k: v for k, v in zip(compile_head, line)}


with open(filename, encoding='utf-8-sig') as rfile, open('new_file.csv', 'w', encoding='utf-8-sig', newline='') as wfile:
    writer = csv.writer(wfile)
    reader = csv.reader(rfile)
    head = next(reader)
    new_head = head[::]
    new_head[new_head.index('salary_from')] = 'salary'
    new_head.remove('salary_to')
    new_head.remove('salary_currency')
    writer.writerow(new_head)
    for row in reader:
        d = {k: v for k, v in zip(head, row)}
        year, month = d['published_at'].split('-')[:2]
        curr_val = compile[year, month]
        new_row = []
        salary = ''
        if (d['salary_from'] != '' or d['salary_to'] != '') and (d['salary_currency'] == "RUR" or (d['salary_currency'] in curr_val and curr_val[d['salary_currency']] != '')):
            salary = 0
            count = 0
            if d['salary_from'] != '':
                salary += float(d['salary_from'])
                count += 1
            if d['salary_to'] != '':
                salary += float(d['salary_to'])
                count += 1
            currency = d['salary_currency']
            if currency != 'RUR':
                salary *= float(curr_val[currency])
            salary //= count

        for k in new_head:
            if k == 'salary':
                new_row.append(salary)
            else:
                new_row.append(d[k])
        writer.writerow(new_row)









