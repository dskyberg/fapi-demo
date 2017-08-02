#!/usr/bin/env python3
import sys
from dateutil import parser
from datetime import datetime
import pytz
import time


def convert_utc_to_local(utc_epoch, time_zone):
    ltz = pytz.timezone(time_zone)
    utc_dt = datetime.fromtimestamp(utc_epoch).replace(tzinfo=pytz.utc)
    local_dt = utc_dt.astimezone(ltz)
    return time.mktime(local_dt.timetuple())


#2017-07-24T12:00:54.297958767Z
def get_utc_epoch(utc_time):

    if isinstance(utc_time, float) or isinstance(utc_time, int):
        return utc_time

    if isinstance(utc_time, str):
        try:
            return int(utc_time)
        except Exception:
            pass
        try:
            return float(utc_time)
        except Exception:
            pass
        try:
            # d = parser.parse(base_time)
            # dstr = utc_time[:26]
            d = datetime.strptime(utc_time[:26], "%Y-%m-%dT%H:%M:%S.%f")
            return time.mktime(d.timetuple())
        except ValueError as e:
            return e

    return Exception("base_time is not an int, float, or str: %s" % type(base_time))


def actualNow(time_zone):
    print('============== Actual UTC ===================')
    ltz = pytz.timezone(time_zone)
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    print('UTC Now:', str(time.mktime(utc_now.timetuple())), utc_now.isoformat())
    print('Local Now:', utc_now.astimezone(ltz).isoformat())
    utc_epoch = get_utc_epoch(utc_now.isoformat())
    base_epoch = convert_utc_to_local(utc_epoch, time_zone)
    print("UTC Converted: ", datetime.fromtimestamp(base_epoch).isoformat())


def native(utc_time_str, time_zone):
    print('============== Native ===================')

    ltz = pytz.timezone(time_zone)
    utc_parsed = datetime.strptime(utc_time_str[:26], "%Y-%m-%dT%H:%M:%S.%f")
    utc_epoch = time.mktime(utc_parsed.timetuple())
    print("Native - UTC parsed: ", str(utc_epoch), utc_parsed.isoformat())

    utc_time = datetime.fromtimestamp(utc_epoch).replace(tzinfo=pytz.utc)
    print("Naive - Reconstituted:", utc_time.isoformat() )
    print("Native - Converted:", utc_time.astimezone(ltz).isoformat())


def main():
    utc_time = sys.argv[1]
    time_zone = 'US/Eastern'
    actualNow(time_zone)
    native(utc_time, time_zone)

    print('============== Methods ===================')

    utc_epoch = get_utc_epoch(utc_time)

    base_epoch = convert_utc_to_local(utc_epoch, time_zone)
    base_time = str(datetime.fromtimestamp(base_epoch))
    print("Argv: %s" % utc_time)
    print("Converted: %s" % base_time)

if __name__ == "__main__":
    main()