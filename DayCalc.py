#!/usr/bin/env python3

__author__ = "Stuart Eichert"
__copyright__ = "Copyright (C) 2021 Stuart Eichert"
__license__ = "Public Domain"
__version__ = "0.1"

"""
Add and Subtract Dates and Days.  See usage() function for more details
"""

from datetime import date
from datetime import datetime
from datetime import timedelta
import os
import sys


def parse_arg(arg):
    if isinstance(arg, int):
        return timedelta(days=arg)
    if arg.lower() == 'today' or arg.lower() == 'now':
        return date.today()
    if arg.lower() == 'tomorrow':
        return date.today() + timedelta(days=1)
    if arg.lower() == 'yesterday':
        return date.today() - timedelta(days=1)
    try:
        ret = datetime.strptime(arg, "%m/%d/%Y")
        return ret.date()
    except ValueError:
        pass
    return timedelta(days=int(arg))


def parse_result(result):
    if isinstance(result, timedelta):
        return result.days
    elif isinstance(result, date):
        return result.strftime("%-m/%-d/%Y")
    return result


def usage(file=sys.stderr, exit_code=1):
    script_name = os.path.basename(sys.argv[0])
    print("""Usage: {0} [-h | --help] date|days +|- date|days

Add/Subtract number of days to a date or the difference between two dates.

Examples:
{0} 2/3/2015 + 100
5/14/2015

{0} 5/25/2015 - 1/4/2014
506

{0} 7/4/2019 - 56
5/9/2019

{0} today + 2
{1}

{0} tomorrow - 3
{2}

{0} yesterday + 1
{3}""".format(script_name,
              process_args([sys.argv[0], 'today', '+', '2']),
              process_args([sys.argv[0], 'tomorrow', '-', '3']),
              process_args([sys.argv[0], 'yesterday', '+', 1])),
          file=file)
    sys.exit(exit_code)


def process_args(argv):
    arg1 = parse_arg(argv[1])
    operation = argv[2]
    arg2 = parse_arg(argv[3])
    result = ''
    if operation == '+':
        if isinstance(arg1, date) and isinstance(arg2, date):
            print("Invalid operation.  You cannot add two dates together.\n", file=sys.stderr)
            usage()
        result = arg1 + arg2
    elif operation == '-':
        if isinstance(arg1, timedelta) and isinstance(arg2, date):
            print("Invalid operation.  You cannot subtract a date from a number of days.\n", file=sys.stderr)
            usage()
        result = arg1 - arg2
    else:
        usage()
    return parse_result(result)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() in ['-h', '--help']:
        usage(sys.stdout, 0)
    if len(sys.argv) < 4:
        usage()
    print(process_args(sys.argv))
