import time
import datetime
def to_seconds(days):
    return days*24*60*60

def sub_check(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    elif middle_time > 0:
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt


