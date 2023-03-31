# import datetime

# def get_dates(num_of_days):
#     today = datetime.date.today()
#     dates = []
#     for i in range(num_of_days):
#         dates.append(datetime.timedelta(days=i) + today)
#     return dates

from datetime import datetime, timedelta

def get_dates(end_date):
    """Generator that yields all days from today until the given end date."""
    current_date = datetime.now().date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    out = []
    while current_date <= end_date:
        out.append(current_date)
        current_date += timedelta(days=1)

    return out