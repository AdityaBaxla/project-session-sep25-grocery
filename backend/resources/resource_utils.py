from datetime import datetime

def validate_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S") # 2025-11-03 17:10:00 format
    except:
        raise ValueError("datetime needs to be in format %Y-%m-%d %H:%M:%S")