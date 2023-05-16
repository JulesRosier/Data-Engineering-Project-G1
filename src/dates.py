from datetime import datetime, timedelta

def get_dates(end_date):
    current_date = datetime.now().date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    out = []
    while current_date <= end_date:
        out.append(current_date)
        current_date += timedelta(days=1)

    return out