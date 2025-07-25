import argparse
from datetime import datetime, date

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD."
        raise argparse.ArgumentTypeError(msg)

# def mkdate(datestr):
#     return datetime.strptime(datestr, '%Y-%m-%d')
# parser.add_argument('--date', '-dt', metavar='DATE', type=mkdate, default=datetime.now(),
#                     help='which date is to retrieve')  

parser = argparse.ArgumentParser()

parser.add_argument('--symbol', type=str, default='tsla',
                    help='a ticker to analyze(default: tsla)')
parser.add_argument("--date", type=valid_date, default=date.today(), 
                    help="Date in YYYY-MM-DD format")      
parser.add_argument('--list', '-l', metavar='LIST', default='test',
                        help='list of stock groups: sp500, dow or all')
parser.add_argument('--batch', type=int, default=0,
                    help='start column (default: 0)')
                        