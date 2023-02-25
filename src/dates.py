import datetime

def get_dates(num_of_days):
    today = datetime.date.today()
    today = datetime.timedelta(days=10) + today
    dates = []
    for i in range(num_of_days):
        dates.append(datetime.timedelta(days=i) + today)
    return dates