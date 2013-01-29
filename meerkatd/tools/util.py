import re
from datetime import datetime
from calendar import timegm
from pytz import UTC


NUM_RE = re.compile('([+-]?\d+) ')
APOS_RE = re.compile("'")


def dBm2i(s):
    m = NUM_RE.match(s)
    if m:
        return int(m.group(0))

    return None


def esc(s):
    return APOS_RE.sub("''", s)


def ts2dt(ts):
    return datetime.fromtimestamp(ts/1000, UTC)


def ts2dates(ts):
    return ts2dt(ts).strftime('%Y-%m-%d %H:%M:%S')


def ts2times(ts):
    return ts2dt(ts).strftime('%H:%M:%S')


def dt2ts(dt):
    return timegm(dt.utctimetuple())*1000


def d2ts(yy, mm, dd, h, m, s, ms=0):
    return dt2ts(datetime(yy, mm, dd, h, m, s, ms, UTC))


def dates2ts(dates):
    return dt2ts(datetime.strptime(dates, '%Y-%m-%d %H:%M:%S'))



