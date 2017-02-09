import datetime
from Config import DELETE_IF_OLDER_THEN
from time import strftime


def date_list():
    keep_dates = []
    t_date = datetime.datetime.now() - datetime.timedelta(days=DELETE_IF_OLDER_THEN)
    date1 = '%s-%02d-%02d' % (t_date.year, t_date.month, t_date.day)
    date2 = strftime("%Y-%m-%d")
    start = datetime.datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.datetime.strptime(date2, '%Y-%m-%d')
    step = datetime.timedelta(days=1)
    while start <= end:
        keep_dates.append(start.date())
        start += step
    return keep_dates


def clear_html():
    list_ok = []
    keep_dates = date_list()
    doc = (open('results.html', "r+"))
    read = doc.readlines()

    for line in read:
        for date in keep_dates:
            date = str(date)
            if date in line and "uplicate" not in line:
                list_ok.append(line)
    doc.close()

    doc = (open('results.html', 'w'))
    for add in list:
        doc.write(add)
    doc.close()

clear_html()