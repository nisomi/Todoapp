from datetime import datetime, timedelta


def get_data():
    day = datetime.now()
    start = day - timedelta(days=day.weekday())
    end = start + timedelta(days=6)

    day_str = day.strftime('%d/%b/%Y')
    start_str = start.strftime('%d %b')
    end_str = end.strftime('%d %b')
    return start_str+ ' - '+end_str