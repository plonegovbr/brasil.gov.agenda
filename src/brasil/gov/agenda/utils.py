# -*- coding: utf-8 -*-
from DateTime import DateTime
from datetime import datetime


def rfc2445dt(value):
    if isinstance(value, datetime):
        value = DateTime(value.strftime('%Y/%m/%d %H:%M'))
    # return UTC in RFC2445 format YYYYMMDDTHHMMSSZ
    return value.HTML4().replace('-', '').replace(':', '')
