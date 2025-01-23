from datetime import datetime
import pytz
def get_current_datetime(timezone_str="Asia/Kathmandu"):
    tz=pytz.timezone(timezone_str)
    return datetime.now(tz=tz).replace(second=0,microsecond=0)